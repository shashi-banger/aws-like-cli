from setuptools import setup
import re
import os
import sys

def get_packages(package):
    """Return root package and all sub-packages."""
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

def get_version(package):
    """Return package version as listed in `__version__` in `init.py`."""
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name="sbaws",
    version=get_version("sbaws"),
    packages=get_packages("sbaws"),
    py_modules=["repo"],
    include_package_data=True,
    install_requires=[
        'click>3.3'
        ],
    entry_points={
        'console_scripts': [ 
            'sbaws = sbaws.__main__:cli'
        ]
    }
)