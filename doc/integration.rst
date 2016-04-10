Integrating PySDL2
==================
PySDL2 consists of two packages, :mod:`sdl2`, which is a plain 1:1 API
wrapper around the SDL2 API, and :mod:`sdl2.ext`, which offers enhanced
functionality for :mod:`sdl2`.

The :mod:`sdl2` package is implemented in a way that shall make it easy for
you to integrate and deploy it with your own software projects. You can rely
on PySDL2 as third-party package, so that the user needs to install it
before he can use your software. Alternatively, you can just copy the
whole package into your project to ship it within your own project
bundle.

.. _importing-pysdl2:

Importing
---------
The :mod:`sdl2` package relies on an external SDL2 library for creating the
wrapper functions. This means that the user needs to have SDL2 installed or
that you ship a SDL2 library with your project.

If the user has a SDL2 library installed on the target system, the
:mod:`ctypes` hooks of :mod:`sdl2` try to find it in the OS-specific standard
locations via :func:`ctypes.util.find_library`. If you are going to ship your
own SDL2 library with the project or can not rely on the standard mechanism of
:mod:`ctypes`, it is also possible to set the environment variable
:envvar:`PYSDL2_DLL_PATH`, which shall point to the directory of the SDL2
library or consist of a list of directories, in which the SDL2 libraries can
be found.

.. note::

   :envvar:`PYSDL2_DLL_PATH` is preferred over the standard
   mechanism. If the module finds a SDL2 library in :envvar:`PYSDL2_DLL_PATH`,
   it will try to use that one in the first place, before using any SDL2
   library installed on the target system.

Let's assume, you ship your own library *SDL2.dll* within your project
location *fancy_project/third_party*. You can set the environment
variable :envvar:`PYSDL2_DLL_PATH` before starting Python. ::

  # Win32 platforms
  set PYSDL2_DLL_PATH=C:\path\to\fancy_project\third_party

  # Unix/Posix-alike environments - bourne shells
  export PYSDL2_DLL_PATH=/path/to/fancy_project/third_party

  # Unix/Posix-alike environments - C shells
  setenv PYSDL2_DLL_PATH /path/to/fancy_project/third_party

  # Define multiple paths to search for the libraries - Win32
  set PYSDL2_DLL_PATH=C:\first\path;C:\second\path

You also can set the environment variable within Python using
:data:`os.environ`. ::

  os.environ["PYSDL2_DLL_PATH"] = "C:\\path\\to\\fancy_project\\third_party"
  os.environ["PYSDL2_DLL_PATH"] = "/path/to/fancy_project/third_party"

.. note::

   If you aim to integrate :mod:`sdl` directly into your software and do
   not want or are not allowed to change the environment variables, you
   can also change the ``os.getenv("PYSDL2_DLL_PATH")`` query within the
   *sdl2/dll.py* (or *sdl2/sdlimage.py*, *sdl2/sdlttf.py*, *sdl2/sdlgfx.py*)
   file to point to the directory, in which you keep the DLL.

Using different SDL2 versions
-----------------------------
PySDL2 tries to provide interfaces to the most recent versions of the
SDL2 libraries. Sometimes this means that PySDL2 tries to test for
functions that might not be available for your very own project or that
are not available on the target system due to a version of the specific
library. To check, if the SDL2 libraries do not provide certain
functions, you can enable the specific warnings for them.

>>> python -W"module"::ImportWarning:sdl2.dll yourfile.py
