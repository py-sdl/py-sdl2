.. module:: sdl2.ext
   :synopsis: Helpful wrappers for the SDL2 API

sdl2.ext - Helpful wrappers for the SDL2 API
============================================

The :mod:`sdl2.ext` module provides a rich set of modules, classes, and
functions for creating games and other applications using PySDL2.

The aim of the `sdl2.ext` module is to wrap commonly-used parts of the SDL2 API
in a more friendly and Pythonic manner, reducing the need for developers to
understand the intricacies of working with ``ctypes`` and making it simpler and
more fun to get PySDL2 programs up and running.

In addition, this module provides a number of template classes and utility
functions for working with colors, input events, file assets, and more.

Due to its broad scope, the :mod:`sdl2.ext` module is divided into a number of
submodules. However, everything in these submodules can be imported directly
from :mod:`sdl2.ext`. For example, ``from sdl2.ext import Window`` is exactly
the same as ``from sdl2.ext.window import Window``.

At present, :mod:`sdl2.ext` contains the following submodules:

.. toctree::
	:maxdepth: 1
	:glob:

	ext/*
