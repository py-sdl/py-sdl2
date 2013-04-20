#!/usr/bin/env python
import sys
from distutils.core import setup

VERSION = "0.1.0"

if __name__ == "__main__":

    if "--format=msi" in sys.argv or "bdist_msi" in sys.argv:
        # hack the version name to a format msi doesn't have trouble with
        VERSIOgbN = VERSION.replace("-alpha", "a")
        VERSION = VERSION.replace("-beta", "b")
        VERSION = VERSION.replace("-rc", "r")

    setupdata = {
        "name":  "PySDL2",
        "version": VERSION,
        "description": "Python SDL2 bindings",
        "author": "Marcus von Appen",
        "author_email": "marcus@sysfault.org",
        "license": "Public Domain / zlib",
        "url": "http://code.google.com/p/py-sdl",
        #"package_dir": {"sdl2.examples": "examples"},
        "package_data": {"sdl2.test": ["resources/*.*"]},
        "packages": ["sdl2",
                     "sdl2.test",
                     "sdl2.test.util",
                     #"sdl2.examples"
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
            "Programming Language :: Python :: Implementation :: CPython",
            "Programming Language :: Python :: Implementation :: IronPython",
            "Programming Language :: Python :: Implementation :: PyPy",
            "Topic :: Software Development :: Libraries :: Python Modules",
            ],
        }
    setup(**setupdata)
