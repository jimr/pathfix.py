#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='pathfix.py',
    version='0.2',
    provides=['pathfix.py'],
    description='Translate OS X / Windows file URLs to directory paths',
    long_description=open('README.rst').read(),
    author='James Rutherford',
    author_email='jim@jimr.org',
    url='https://github.com/jimr/pathfix.py',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        ],
    license='MIT',
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'pathfix = pathfix:main',
        ]
    },
)
