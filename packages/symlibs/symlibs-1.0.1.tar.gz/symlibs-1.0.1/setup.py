#!/usr/bin/python
# coding=utf-8

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'symlibs',
    version = '1.0.1',
    author = 'diannaojun',
    url = 'http://',
    author_email = 'aheiwuchang@163.com',
    description = '',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    package_dir = {"" : "src"},
    packages = setuptools.find_packages(where = "src"),
    python_requires = ">=3.12",
    install_requires = [
        # 依赖列表
    ],
)
