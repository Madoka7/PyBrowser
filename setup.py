#!/usr/bin/env python3
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.readlines()

setup(
    name='PyBrowser',
    version='0.1.4',
    author='spengx',
    author_email='ss@uutoto.com',
    packages=find_packages(),
    keywords="browser spider",
    install_requires=requirements,
    include_package_data=True,
    license='MIT License',
)
