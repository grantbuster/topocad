"""
setup.py
"""
import os
from codecs import open
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from subprocess import check_call
import shlex
from warnings import warn

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    readme = f.read()

with open("requirements.txt") as f:
    install_requires = f.readlines()

description = ('Topography-based 3D modeling using CAD + python '
               'scripting tools.')

setup(
    name="topocad",
    version='0.0.0',
    description=description,
    long_description=readme,
    author="Grant Buster",
    author_email="grant.buster@gmail.com",
    url="https://github.com/grantbuster/topocad",
    packages=find_packages(),
    package_dir={"topocad": "topocad"},
    include_package_data=True,
    license="MIT License",
    zip_safe=False,
    keywords="topocad",
    python_requires='>=3.9',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    install_requires=install_requires,
)
