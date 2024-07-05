# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name="kjsonForPython",
    version="1.0.0",
    keywords=["kjson", "json", "javascript", "network"],
    description="A json library for python, which can be used in network communication",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    author="kuankuan",
    author_email="2163826131@qq.com",
    url="https://github.com/kuankuan2007/kjson-for-python/",
    install_requires=[],
    long_description_content_type="text/markdown",
    packages=["kjsonForPython"],
    license="Mulan PSL v2",
    platforms=["windows", "linux", "macos"],
    classifiers=[
        "Natural Language :: English",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: Mulan Permissive Software License v2 (MulanPSL-2.0)",
    ],
)
