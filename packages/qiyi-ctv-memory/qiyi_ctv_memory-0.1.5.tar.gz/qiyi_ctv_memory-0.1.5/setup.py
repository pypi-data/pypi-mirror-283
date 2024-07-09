# -*- coding: utf-8 -*--
from setuptools import setup, find_packages

setup(
    name='qiyi_ctv_memory',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        "argparse", "numpy"
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