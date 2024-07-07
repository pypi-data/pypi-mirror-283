#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys


if len(sys.argv) <= 1:
    print("""
Suggested setup.py parameters:

    * build
    * install
    * sdist  --formats=zip
    * sdist  # NOTE requires tar/gzip commands

    python -m pip install -e .

PyPi:

    python -m pip install setuptools twine

    python setup.py sdist
    python twine upload dist/* --verbose

    ./setup.py  sdist ; twine upload dist/* --verbose

""")

readme = open('README.rst').read()

setup(
    name='text_histogram32',
    version='0.0.7',
    description='A dependency-free library to quickly make ascii/text histograms from data.',
    long_description=readme,
    author='Andy Kish, Jehiah Czebotar, Jay Deiman, Jon Lundy, Chris Clark',
    url='https://github.com/clach04/text_histogram32',
    py_modules=['text_histogram'],
    license='Apache License, Version 2.0',
    zip_safe=True,
    classifiers=[  # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Terminals',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    platforms='any',
)
