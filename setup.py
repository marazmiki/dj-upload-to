#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals, print_function
import os
import sys
import dj_upload_to
import setuptools
import setuptools.command.test


ROOT_PACKAGE = 'dj-upload-to'
VERSION = dj_upload_to.__version__
DESCRIPTION = 'Small application that simplifies naming of uploaded files'
DIR = os.path.dirname(__file__)


class pytest(setuptools.command.test.test):
    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)
        self.pytest_args = ['tests.py']

    def run_tests(self):
        import pytest as _pytest
        sys.exit(_pytest.main(self.pytest_args))


def long_description():
    """
    Returns package long description from README
    """
    def read(what):
        with open(os.path.join(DIR, '{}.rst'.format(what))) as fp:
            return fp.read()
    return '{README}\n\n{CHANGELOG}'.format(
        README=read('README'),
        CHANGELOG=read('CHANGELOG'),
    )


if __name__ == '__main__':
    setuptools.setup(
        name=ROOT_PACKAGE,
        description=DESCRIPTION,
        author='Mikhail Porokhovnichenko',
        author_email='marazmiki@gmail.com',
        url='https://github.com/marazmiki/dj-upload-to',
        license='MIT',
        version=VERSION,
        long_description=long_description(),
        py_modules=['dj_upload_to'],
        extras_require={
            'tests': ['pytest', 'coverage', 'coveralls', 'flake8'],
        },
        test_suite='tests',
        cmdclass={'test': pytest},
        zip_safe=False,
        classifiers=[
            'Environment :: Web Environment',
            'Framework :: Django',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy',
            'Operating System :: OS Independent',
        ]
    )
