#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup

version = {}
with open("rsapp/version.py") as fp:
    exec(fp.read(), version)
# later on we use: version['__version__']

setup(
    name='rspub-gui',
    version=version['__version__'],
    packages=['rsapp.gui'],
    url='https://github.com/EHRI/rspub-gui',
    license='Apache License 2.0',
    author='henk van den berg',
    author_email='henk.van.den.berg at dans.knaw.nl',
    description='Application for ResourceSync publishing',
    install_requires=['rspub-core', 'pyqt5']
)
