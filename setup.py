#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup
from rsapp import version

setup(
    name='rspub-gui',
    version=version.__version__,
    packages=['rsapp.gui'],
    url='https://github.com/EHRI/rspub-gui',
    license='Apache License 2.0',
    author='henk van den berg',
    author_email='henk.van.den.berg at dans.knaw.nl',
    description='Application for ResourceSync publishing',
    install_requires=['rspub-core', 'pyqt5']
)
