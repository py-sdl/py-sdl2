Release News
============
This describes the latest changes between the PySDL2 releases.

0.4.0
-----
Released on 2013-XX-XX.

* issue #1: fixed libc loading for cases where libc.so is a ld script

0.3.0
-----
Released on 2013-05-07.

* new :mod:`sdl2.sdlgfx` module, which provides access to the SDL2_gfx library
* new :mod:`sdl2.ext.UIFactory.from_color` method; it creates UI-supportive
  sprites from a color
* fixed color argument bugs in :class:`sdl2.ext.RenderContext` methods
* fixed a module namespace issues in :mod:`sdl2.ext.pixelaccess`
* :mod:`sdl2.ext.SpriteFactory` methods do not use a default ``size`` argument
  anymore; it has to provided by the caller


0.2.0
-----
Released on 2013-05-03.

* removed sdl2.ext.scene; it now lives in python-utils
* fixed :mod:`sdl2.haptic` module usage for Python 3
* fixed :func:`sdl2.SDL_WindowGetData` and :func:`sdl2.SDL_WindowSetData`
  wrappers
* fixed :meth:`sdl2.ext.RenderContext.copy`
* fixed :mod:`sdl2.ext.font` module usage for Python 3
* fixed :func:`sdl2.ext.line`
* :mod:`sdl2` imports all submodules now
* improved documentation

0.1.0
-----
Released on 2013-04-23.

* Initial Release
