"""
    文本预处理库
"""
import cn2an

import re

import pre_process_chain.dd.symbol_convert as symbol_convert
import pre_process_chain.dd.frequent_chars as frequent_chars
import pre_process_chain.dd.chinese_digits as chinese_digits

from typing import Tuple


class RegexReplacer:
    """
        输入一个key为正则表达式的词典，通过分组的方式，只需执行一次正则，即可多模匹配批量替换

        Parameters
        ----
        replace_map: key为正则表达式的词典，形如{r"regex": "需要替换的字段"}

        Examples
        ----
        >>> replace_map = {"替换前": "替换后"}
        >>> RegexReplacer(replace_map).sub("替换前")
        '替换后'
    """

    def __init__(self, replace_map: dict):
        self.data = replace_map
        self.dict_keys = list(replace_map.keys())
        self._len = len(self.dict_keys)
        self.regex = re.compile("|".join(["(%s)" % s for s in self.dict_keys]))

    def sub(self, sentence: str) -> str:
        """
        将字符串中命中的正则表达式进行批量替换

        :param sentence: 原始字符串
        :return: 替换后的字符串
        """
        return re.sub(self.regex,
                      lambda x: self.data.get(self.dict_keys[x.group(*range(1, self._len + 1)).index(x.group(0))], ""),
                      sentence)


class TextProcess:
    """
        文本预处理器，直接通过类方法调用需要的方法即可
        调用: TextProcess.function(*args, **kwargs)
    """
    convert_dict = (dict(zip(frequent_chars.data, frequent_chars.data)))
    convert_dict.update(symbol_convert.data)
    convert_dict.update(chinese_digits.data)
    convert_dict_ambiguous = convert_dict.copy()
    convert_dict_ambiguous.update(chinese_digits.data_ambiguous)
    replacer_digits = RegexReplacer(chinese_digits.data_precise)
    regex_html_tag = re.compile(r"</?(?:p|b|span|br|div|li|ui|h).*?>|&nbsp;")

    @classmethod
    def remove_html_tag(cls, sentence: str) -> str:
        sentence = re.sub(cls.regex_html_tag, "", sentence)
        return sentence

    @classmethod
    def purify(cls, sentence: str, allow_ambiguous=False) -> str:
        """
        去除生僻字，仅保留常用汉字和常用标点符号，大写转小写，全角转半角，特殊数字转普通数字，部分繁体数字转简体数字

        :param sentence: 原始字符串
        :param allow_ambiguous: 启用allow_ambiguous在模糊模式下则可能产生歧义，如“海陆”替换为“海六”，准确模式下则只会将“陆七八”替换为“六七八”，但是由于使用到正则性能会下降
        :return: 净化后的字符串
        """
        if re.findall(r"[，。！？]", sentence):  # 若出现全角符号，则再出现前后非英文的半角句点认为其等同于逗号
            sentence = re.sub(r"(?<![a-zA-Z])\.(?![a-zA-Z])", ",", sentence)

        use_dict = cls.convert_dict_ambiguous if allow_ambiguous else cls.convert_dict
        new_sentence = []
        for i in range(len(sentence)):
            new_sentence.append(use_dict.get(sentence[i], ""))
        sentence = "".join(new_sentence)
        sentence = re.sub(cls.regex_html_tag, "", sentence)
        return sentence if allow_ambiguous else cls.replacer_digits.sub(sentence)

    regex_para_sep = re.compile(
        r"(?<!\d)\.(?!net|js)|[。？！?!]|\t|\\t|\r|\\r|\n|\\n|(?<!\d)[1-9][.、,)]")  # 句号分隔符，预编译正则，静态成员只编译一次，提高执行效率
    regex_comma_sep = re.compile(r"(?<!\d),|[，:：;；]")  # 逗号分隔符
    regex_illegal_filter = re.compile(r"(?<![a-z\d])\s(?![a-z\d])")  # 非英文数字连接的空格
    regex_light_split = re.compile(r"[\s]")  # 空格

    @classmethod
    def scan_separator(cls, sentence: str, comma_sep="，", para_sep="|") -> str:
        """
        扫描输入句中的分割符，替换为形如"这是一句句子|这是另一句句子"的形式

        :param sentence: 原始字符串
        :param comma_sep: 函数将逗号分隔符替换为该参数
        :param para_sep: 函数将句号分隔符替换为该参数，如该参数中出现顿号"、"则可能导致问题，使用其他字符替代
        :return: 替换后的字符串
        """
        original = sentence
        sentence = re.sub(cls.regex_para_sep, "|", sentence)
        sentence = re.sub(cls.regex_comma_sep, "、", sentence)
        if original != sentence:
            sentence = re.sub(cls.regex_illegal_filter, "", sentence)  # 已经检测到标点符号，去除掉多余的符号
        else:  # 输入中没有标点符号，认为输入形如"这句句子 用空格分割"、"一项+另一项"以空格或加号分隔
            sentence = re.sub(cls.regex_light_split, "、", sentence)
        sentence = sentence.strip("、").strip("|")
        sentence = re.sub(r"\|+", para_sep, sentence)
        sentence = re.sub(r"、+", comma_sep, sentence)
        return sentence

    continuous_symbol_replacer = RegexReplacer({r"[\-~]+": "-", r"\s+": " "})

    @classmethod
    def replace_continuous_symbol(cls, sentence: str) -> str:
        """
        替换连续字符，如将"--~"替换为"-"，"   "替换为" "

        :param sentence: 原始字符串
        :return: 替换后的字符串
        """
        return cls.continuous_symbol_replacer.sub(sentence)

    regex_digits_with_dot = re.compile(r"(?<=\d)(\.\d+)")
    regex_digits_with_comma_10k = re.compile(r"(?<!\d)(\d{1,2}),(\d{3})(?!\d)")
    regex_digits_with_comma_100k = re.compile(r"(?<!\d)(\d{3}),(0{3})")

    chinese_digit_replacer = RegexReplacer(chinese_digits.data_numerical)
    regex_multiple_chinese_digit = re.compile(r"([一二三四五六七八九])个([零一二三四五六七八九])")

    @classmethod
    def numerate_chinese_digit(cls, sentence: str) -> str:
        """
        将中文零到九转换为阿拉伯数字，若出现如"三个零"的表述，将替换为"000"

        :param sentence: 原始字符串
        :return: 替换后的字符串
        """
        sentence = cn2an.transform(sentence)  # 注：使用该库"半"会被替换为"0.5"
        sentence = re.sub(
            cls.regex_multiple_chinese_digit,
            lambda x: (
                    int(chinese_digits.data_numerical.get(x.group(1))) * chinese_digits.data_numerical.get(x.group(2))
            ),
            sentence
        )
        sentence = cls.chinese_digit_replacer.sub(sentence)
        return sentence

    regex_chinese_digit = re.compile(r"[零一二三四五六七八九]")

    @classmethod
    def chinese_digit_count(cls, sentence: str) -> int:
        """
        统计一个字符串中出现的零到九的次数

        :param sentence: 需统计字符串
        :return: 出现中文数字字符的个数
        """
        return len(re.findall(cls.regex_chinese_digit, sentence))

    @classmethod
    def regulate_digits(cls, sentence: str, keep_decimal=True) -> str:
        """
        将字符串中带有逗号或句号的数字整数化，如"3,500.50---4,000.00"转换为"3500-4000"

        :param sentence: 原始字符串
        :param keep_decimal: 是否移除小数点后的数字
        :return: 部分数字被正规化的字符串
        """
        sentence = cls.replace_continuous_symbol(sentence)
        if not keep_decimal:
            sentence = re.sub(cls.regex_digits_with_dot, r"", sentence)
        sentence = re.sub(cls.regex_digits_with_comma_10k, r"\g<1>\g<2>", sentence)
        sentence = re.sub(cls.regex_digits_with_comma_100k, r"\g<1>\g<2>", sentence)
        return sentence

    @staticmethod
    def sub_extract(pattern: str, string: str) -> Tuple[str, list]:
        """
            将输入文本中，符合模式的部分提取出并替换为空
        :param pattern: 需要提取的模式
        :param string: 输入文本
        :return: (被提取后的串, 抽取的匹配项列表)
        """
        collection = []

        def repl_and_extract(matched):
            collection.append(matched[0])
            return " "

        return re.sub(pattern, lambda x: repl_and_extract(x), string), collection
