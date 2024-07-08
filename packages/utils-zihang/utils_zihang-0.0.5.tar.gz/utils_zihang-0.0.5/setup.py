# -*- coding:utf-8 -*-
"""
Created on 2023/7/26 17:45
@File: setup.py
---------
@summary:
---------
@Author: luzihang
@Contact: https://github.com/luzihang123
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utils_zihang",
    version="0.0.5",
    author="zihang",
    author_email="clark1203@foxmail.com",
    description="工具方法",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "loguru==0.6.0",
        "pymongo==4.8.0"
    ],
    python_requires='>=3',
)
