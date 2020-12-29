#!/usr/bin/env python
import re

try:
    from setuptools import setup
    from setuptools.command.sdist import sdist
except ImportError:
    from distutils.core import setup
    from distutils.command.sdist import sdist


cmdclass = {}


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')
    history = re.sub(r':\w+:`(\w+(?:\.\w+)*)`', r'``\1``', history)

requirements = [
    'coolname>=1.1,<1.2'
]


setup(
    name='coolname-hash',
    version='1.1.1',
    description="Human-readable pseudo-hash, based on coolname.",
    long_description=readme + '\n\n' + history,
    author="Alexander Lukanin",
    author_email='alexander.lukanin.13@gmail.com',
    url='https://github.com/alexanderlukanin13/coolname_hash',
    py_packages=[
        'coolname_hash',
    ],
    cmdclass=cmdclass,
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=True,
    keywords=['coolname', 'hash', 'pseudohash'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
