#!/usr/bin/env python3
import PyBrowser
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name='PyBrowser',
    version=PyBrowser.__version__,
    author=PyBrowser.__author__,
    author_email=PyBrowser.__author_email__,
    packages=find_packages(),
    keywords="browser spider",
    install_requires=requirements,
    include_package_data=True,
    license='MIT License',
)
