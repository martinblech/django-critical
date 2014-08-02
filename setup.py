#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


setup(
    name='django-critical',
    version='0.1',
    description=('Inlines critical path CSS and defers loading full CSS '
                 'asynchronously.'),
    author='Martin Blech',
    author_email='martinblech@gmail.com',
    url='https://github.com/martinblech/django-critical',
    long_description=open('README.md', 'r').read(),
    packages=[
        'critical',
        'critical.templatetags',
    ],
    package_data={
        'critical': [
            'templates/critical/*',
        ]
    },
    zip_safe=False,
    install_requires=[
        'django-appconf >= 0.4',
        'cssmin >= 0.2.0',
    ],
    tests_require=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
