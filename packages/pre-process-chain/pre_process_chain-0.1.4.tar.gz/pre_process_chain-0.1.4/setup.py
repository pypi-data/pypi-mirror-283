from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pre_process_chain',  # 包名
    version='0.1.4',  # 版本号
    description='包含一种链式预处理设计模式（以更低的时间成本解决同时需要多种预处理方式的场景）、以及实现了一些文本预处理方法的包',
    long_description=long_description,
    author='ray.ping',
    author_email='342099577@qq.com',
    url='',
    install_requires=[
        'cn2an >= 0.5.22'
    ],  # 依赖包会同时被安装
    license='MIT',
    packages=find_packages()
)
