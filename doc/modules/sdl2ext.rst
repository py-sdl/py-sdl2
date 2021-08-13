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


SDL2 module wrappers
--------------------

Some parts of the :mod:`sdl2.ext` module contain Pythonic wrappers for common
and/or unpleasant parts of the SDL2 API. At present, these modules include:

.. toctree::
	:maxdepth: 1

	ext/common.rst
	ext/window.rst
	ext/msgbox.rst
	ext/renderer.rst


Utilities for working with SDL2 in Python
-----------------------------------------

Other parts of this module implement functions and classes that make it easier
to work with SDL2 functions and data structures in Python (and vice versa).
These include functions for converting text to and from UTF8-encoded bytes,
reading and writing ``ctypes`` arrays, and casting :obj:`~sdl2.SDL_Surface`
objects to Numpy arrays:

.. toctree::
	:maxdepth: 1

	ext/compat.rst
	ext/array.rst
	ext/pixelaccess.rst


SDL2-based extensions
---------------------

In addition to simple Pythonic wrappers for SDL2 functions and structures, the
:mod:`sdl2.ext` module also offers a number of  high-level classes and functions
that use SDL2 internally to provide APIs for font rendering, building GUIs,
importing images, and more:

.. toctree::
	:maxdepth: 1

	ext/image.rst
	ext/spritesystem.rst
	ext/gui.rst
	ext/font.rst
	ext/draw.rst
	ext/surface.rst


Useful helpers for building apps
--------------------------------

Beyond wrappers and utilities for working with SDL2's API, the
:mod:`sdl2.ext` module also includes a number of submodules with various
functions and classes to help facilitate general game and app development with
PySDL2. These include classes for writing games using component-oriented
programming, managing program resource files, working with colors, and more:

.. toctree::
	:maxdepth: 1

	ext/resources.rst
	ext/ebs.rst
	ext/events.rst
	ext/color.rst
	ext/colorpalettes.rst
	ext/algorithms.rst
	ext/particles.rst
