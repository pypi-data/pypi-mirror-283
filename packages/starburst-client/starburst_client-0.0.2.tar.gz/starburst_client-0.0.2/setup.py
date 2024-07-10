#!/usr/bin/env python

from setuptools import setup

with open("README.md", "rb") as f:
    readme = f.read().decode("utf-8")

about: dict[str, str] = {}
with open("starburst_client/_version.py", "rb") as f:
    exec(f.read(), about)


tests_require = ["pytest"]

setup(
    name=about["__title__"],
    version=about["__version__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    license=about["__license__"],
    python_requires=">=3.6, <4",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
    packages=["starburst_client"],
    install_requires=["requests"],
    extras_require={
        "test": tests_require,
    },
    tests_require=tests_require,
    test_suite="tests",
)
