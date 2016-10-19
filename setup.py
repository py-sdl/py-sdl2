#!/usr/bin/env python
import os
import sys
from distutils.core import setup

VERSION = "0.9.5"

if __name__ == "__main__":

    if "--format=msi" in sys.argv or "bdist_msi" in sys.argv:
        # hack the version name to a format msi doesn't have trouble with
        VERSION = VERSION.replace("-alpha", "a")
        VERSION = VERSION.replace("-beta", "b")
        VERSION = VERSION.replace("-rc", "r")

    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.txt")
    readme = open(fname, "r")
    long_desc = readme.read()
    readme.close()

    setupdata = {
        "name":  "PySDL2",
        "version": VERSION,
        "description": "Python SDL2 bindings",
        "long_description": long_desc,
        "author": "Marcus von Appen",
        "author_email": "marcus@sysfault.org",
        "license": "Public Domain / zlib",
        "url": "http://bitbucket.org/marcusva/py-sdl2",
        "download_url": "http://bitbucket.org/marcusva/py-sdl2/downloads",
        "package_dir": {"sdl2.examples": "examples"},
        "package_data": {"sdl2.test": ["resources/*.*"],
                         "sdl2.examples": ["resources/*.*"]},
        "packages": ["sdl2",
                     "sdl2.ext",
                     "sdl2.test",
                     "sdl2.test.util",
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
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ],
        }
    setup(**setupdata)
