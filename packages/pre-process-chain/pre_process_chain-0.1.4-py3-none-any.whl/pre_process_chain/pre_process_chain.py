"""
    链式预处理，有些情况下可能需要多种不同的文本预处理，该类会存储每一个预处理步骤的结果，以供复用

    # 初始化实例，声明有哪些预处理方法及这些方法的别名
    pre_process_chain = PreProcessChain({
        "purify": TextProcess.purify,
        "numerate": TextProcess.numerate_chinese_digit,
        "separate": lambda x: TextProcess.scan_separator(x, " ", "|")
    })

    # 对某段文本指定某些预处理方法，若是多个预处理方法串行执行时用"-"连接
    result = pre_process_chain.generate(text, ["purify-numerate", "purify-separate"])

    # 获取某种方法的预处理结果
    result.get("purify")
    result.get("purify-numerate")
"""

from typing import List


class PreProcessResult:
    def __init__(self, generate_result: dict):
        """
            预处理结果树对象，用于解析和方便获取生成结果
        :param generate_result: 预处理生成器的结果
        """
        self.value = generate_result

    def get(self, alias: str):
        """
            用于获取预处理结果，当预处理文本是多个方法顺序连接时，需传入形如"alias1-alias2"用"-"连接的名称
        :param alias:
        :return: 指定预处理链的预处理结果
        """
        alias_to_iterate = alias.split("-")
        node = self.value
        for iterate in alias_to_iterate:
            node = node.get(iterate, node)
        return node[PreProcessChain.RESULT_FIELD]


class PreProcessChain:
    RESULT_FIELD = 0

    def __init__(self, methods: dict):
        """
            告知预处理构造器可以使用那些预处理方法，传入{别名: 方法}词典
        :param methods: 别名:方法 形如{"alias": TextProcess.func}，注：alias中"-"有特殊用途，所以若使用则将被转义为"_"
        """
        self.methods = {k.replace("-", "_"): v for k, v in methods.items()}

    def generate(self, text: str, use_methods: List[str]) -> PreProcessResult:
        """
            传入需要预处理文本，并告知方法需要用那些预处理手段，若有多个预处理手段顺序连接时需使用"alias1-alias2"，用"-"连接的格式传入
        :param text: 需被预处理的文本
        :param use_methods: 需要预处理的方法别名，若为多个方法顺序连接，使用"-"连接，如"alias1-alias2"，则会依次执行预处理方法
        :return: 树状结构，如{"alias1": {"result": "预处理文本1", "alias2": {"result": "预处理文本2"}}}，预处理文本2表示经过alias1和alias2顺序处理的结果
        """
        result = {}
        for method_chain in use_methods:
            list_method_chain = method_chain.split("-")
            buffer = text  # 存储中间处理状态
            result_node = result
            for method in list_method_chain:
                result_node[method] = result_node.get(method, {})
                if result_node[method]:  # 若已经存在则使用已经存在的结果
                    buffer = result_node[method][self.RESULT_FIELD]
                else:  # 若不存在，则调用预处理方法生成
                    buffer = self.methods.get(method)(buffer)
                    result_node[method] = {self.RESULT_FIELD: buffer}
                result_node = result_node[method]  # 向下遍历
        return PreProcessResult(result)
