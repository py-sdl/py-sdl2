Installing PySDL2
=================
This section provides an overview and guidance for installing PySDL2 on
various target platforms.

Getting the sources
-------------------
You can download the official releases of PySDL2 from
https://github.com/marcusva/py-sdl2/releases. Download the most
recent release, unpack it and make sure that you installed the relevant
prerequisites before continuing with the installation.

Prerequisites
-------------
PySDL2 relies on some 3rd party packages to be fully usable and to
provide you full access to all of its features.

You must have at least one of the following Python versions installed:

* Python 2.7, 3.5+     (http://www.python.org)
* PyPy 1.8.0+          (http://www.pypy.org)

Other Python versions or Python implementations might work, but are
(currently) not officially tested or supported by the PySDL2
distribution.

You need to have a working SDL2 library on your target system. You can obtain
the source code (to build it yourself) or a prebuilt version at
http://www.libsdl.org. Alternatively, on macOS and Windows, you can install
the SDL2 binaries for PySDL2 using pip via the pysdl2-dll package.

PySDL2 also offers support for the following SDL-related libraries:

* SDL2_image             (http://www.libsdl.org/projects/SDL_image/)
* SDL2_mixer             (http://www.libsdl.org/projects/SDL_mixer/)
* SDL2_ttf               (http://www.libsdl.org/projects/SDL_ttf/)
* SDL2_gfx               (http://www.ferzkopp.net/Software/SDL_gfx-2.0/)

Those are optional though and only necessary if you want to use
:mod:`sdl2.sdlimage`, :mod:`sdl2.sdlmixer`, :mod:`sdl2.sdlttf` or
:mod:`sdl2.sdlgfx`.

Installation
------------
You can either use the python way of installing the package or the make
command using the Makefile on POSIX-compatible platforms, such as Linux
or BSD, or the make.bat batch file on Windows platforms.

Simply type ::

  python setup.py install

for the traditional python way or ::

  make install

for using the Makefile or make.bat. Both will try to perform a default
installation with as many features as possible.

Trying out
^^^^^^^^^^
You also can test out PySDL2 without actually installing it. You just
need to set up your ``PYTHONPATH`` to point to the location of the
source distribution package. On Windows-based platforms, you might use
something like ::

   set PYTHONPATH=C:\path\to\pysdl2\:%PYTHONPATH%

to define the ``PYTHONPATH`` on a command shell. On Linux/Unix, use ::

   export PYTHONPATH=/path/to/pysdl2:$PYTHONPATH

for bourne shell compatibles or ::

   setenv PYTHONPATH /path/to/pysdl2:$PYTHONPATH

for C shell compatibles. You can omit the `:$PYTHONPATH`, if you did not use
it so far and if your environment settings do not define it.

.. note::

   If you did not install SDL2 using the preferred way for your operation
   system, please read the information about :ref:`importing-pysdl2` in the
   section :doc:`integration`.
