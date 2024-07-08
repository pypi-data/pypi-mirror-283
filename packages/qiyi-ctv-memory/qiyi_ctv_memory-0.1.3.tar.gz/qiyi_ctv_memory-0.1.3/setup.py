# -*- coding: utf-8 -*--
from setuptools import setup, find_packages

setup(
    name='qiyi_ctv_memory',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        # 在这里列出你的依赖包
    ],
    license='IQIYI License',
    author='MaoYongPeng',
    author_email='maoyongpeng@qiyi.com',
    description='内存相关测试工具',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://gitlab.qiyi.domain/ctv-performance/GalaApmScript',
    classifiers=[

    ],
    python_requires='>=2.7',
)