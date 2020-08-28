#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 23:40:44 2020

@author: nick
"""

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="cbapi-nickruedlinger", # Replace with your own username
    version="0.0.1",
    author="Nick Rüdlinger",
    description="simple api for crunchbase free version",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nickruedlinger/cbapi",
    packages=setuptools.find_packages(),
    install_requires = ["pandas", "requests"]
)