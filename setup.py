#!/usr/bin/env python3
"""
Setup script for Sleeper Fantasy Pick'em Skins Game Automation
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pickem-fantasy-automation",
    version="1.0.0",
    author="Sankalan Sarbadhikari",
    author_email="sankalans@gmail.com",
    description="A Python package for automating fantasy football skins game calculations using the Sleeper API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nalaknas/pickem-fantasy-automation",
    project_urls={
        "Bug Reports": "https://github.com/nalaknas/pickem-fantasy-automation/issues",
        "Source": "https://github.com/nalaknas/pickem-fantasy-automation",
        "Contact": "mailto:sankalans@gmail.com",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pickem-automation=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
