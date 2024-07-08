from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='pickle_tool',  # 包名
    version='0.1.0',  # 版本号
    description='基于pickle的拓展工具',
    long_description=long_description,
    author='ray.ping',
    author_email='342099577@qq.com',
    url='',
    license='MIT',
    packages=find_packages()
)
