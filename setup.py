#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import critical

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = critical.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-critical',
    version=version,
    description="""Inlines critical path CSS and defers loading full CSS asynchronously.""",
    long_description=readme + '\n\n' + history,
    author='Martín Blech',
    author_email='martinblech@gmail.com',
    url='https://github.com/martinblech/django-critical',
    packages=[
        'critical',
        'critical.templatetags',
    ],
    include_package_data=True,
    install_requires=[
        'django-appconf >= 0.4',
        'cssmin >= 0.2.0',
    ],
    license="MIT",
    zip_safe=False,
    keywords='django-critical',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
