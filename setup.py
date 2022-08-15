#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, io, pkg_resources, setuptools, numpy as np
#from skbuild import setup
from distutils import util

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(os.path.join(__location__, 'Version'), "r+") as f:
    Version = f.read().rstrip("\n").split(".")
    Major, Mid, Minor = int(Version[0]), int(Version[1]), int(Version[2])

if '--NewMajor' in sys.argv:
    Major += 1
    sys.argv.remove('--NewMajor')
if '--NewMid' in sys.argv:
    Mid += 1
    sys.argv.remove('--NewMidr')
if '--NewMinor' in sys.argv:
    Minor += 1
    sys.argv.remove('--NewMinor')

Version = f'{Major}.{Mid}.{Minor}'

print(f"PyFinitDifference Version: {Version}")

with open(os.path.join(__location__, 'Version'), "w+") as f:
    f.writelines(Version)


plateform = util.get_platform().replace("-", "_")

requirementPath = os.path.join(os.path.dirname(__file__), 'requirements.txt')
here = os.path.abspath(os.path.dirname(__file__))

with open(requirementPath, 'r') as requirements_txt:
    REQUIRED = [str(requirement)
                for requirement in pkg_resources.parse_requirements(requirements_txt)]

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


def _find_packages():
    packages = setuptools.find_packages()
    print("--"*50 + "\n Added files:\n", packages, "--"*50)
    return packages


setuptools.setup(
    name                          = 'PyFinitDifference',
    version                       = Version,
    description                   = 'A package for light scattering simulations.',
    long_description              = long_description,
    long_description_content_type = 'text/markdown',
    author                        = 'Martin Poinsinet de Sivry',
    author_email                  = 'Martin.poinsinet.de.sivry@gmail.com',
    setup_requires                = ['numpy', 'pybind11'],
    python_requires               = '>=3.6',
    url                           = 'https://github.com/MartinPdeS/PyMieSim',
    packages                      = _find_packages(),
    install_requires              = REQUIRED,
    extras_require                = {},
    dependency_links              = [],
    include_package_data          = True,
    license                       = 'MIT',
    package_data                  = {'PyMieSim': ['requirements.txt', "*.for"]},
    classifiers=[  # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
                                    'License :: OSI Approved :: MIT License',
                                    'Operating System :: Unix',
                                    'Operating System :: Microsoft :: Windows',
                                    'Operating System :: MacOS',
                                    'Programming Language :: Python',
                                    'Programming Language :: Python :: 3',
                                    'Programming Language :: Python :: 3.8',
                                    'Programming Language :: Python :: 3.9',
                                    'Programming Language :: Python :: Implementation :: CPython',
                                    'Development Status :: 3 - Alpha',
                                    'Topic :: Scientific/Engineering :: Physics',
                                    'Intended Audience :: Science/Research',
                                ],

)
