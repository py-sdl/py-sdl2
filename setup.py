#!/usr/bin/env python
import os
import sys
import re
from setuptools import setup

VERSION = "0.9.18a1"

if __name__ == "__main__":

    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
    with open(fname, "r") as readme:
        long_desc = readme.read()
        # Strip out CI badges for PyPI releases
        long_desc = re.sub(r"\[!\[Build Status(.*?)\n", "", long_desc)

    setupdata = {
        "name":  "PySDL2",
        "version": VERSION,
        "description": "Python SDL2 bindings",
        "long_description": long_desc,
        "long_description_content_type": "text/markdown",
        "author": "Marcus von Appen",
        "author_email": "marcus@sysfault.org",
        "license": "Public Domain / zlib",
        "url": "https://github.com/py-sdl/py-sdl2",
        "download_url": "https://pypi.python.org/pypi/PySDL2",
        "package_dir": {"sdl2.examples": "examples"},
        "package_data": {"sdl2.test": ["resources/*.*"],
                         "sdl2.examples": ["resources/*.*"]},
        "packages": ["sdl2",
                     "sdl2.ext",
                     "sdl2.test",
                     "sdl2.examples"
                     ],
        "classifiers": [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "License :: Public Domain",
            "License :: OSI Approved :: zlib/libpng License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ],
        }
    setup(**setupdata)
