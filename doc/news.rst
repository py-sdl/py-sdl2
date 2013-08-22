Release News
============
This describes the latest changes between the PySDL2 releases.

0.5.0
-----
Released on 2013-08-14.

* new :class:`sdl2.ext.FontManager` class, which provides simple TTF font
  rendering.
* new :meth:`sdl2.ext.SpriteFactory.from_text()` method, which creates
  text sprites
* put the SDL2 dll path at the beginning of PATH, if a PYSDL2_DLL_PATH
  is provided to avoid loading issues for third party DLLs on Win32
  platforms
* minor documentation fixes

Thanks to Dan Gillett for providing the FontManager and from_text()
enhancements and his patience regarding all the small change requests.
Thanks to Mihail Latyshov for providing fixes to the documentation.


0.4.1
-----
Released on 2013-07-26.

* updated :mod:`sdl2` to include the latest changes of SDL2
* improved DLL detection for DLLs not being in a library path
* fixed a bug in :meth:`sdl2.ext.RenderContext.draw_rect()` for drawing
  a single rect
* fixed a bug in the :func:`repr` call for :class:`sdl2.ext.SoftwareSprite`
* issue #4: fixed a bug in :meth:`sdl2.ext.RenderContext.fill()` for filling
  a single rect
* issue #5: fixed pip installation support
* issue #6: fixed a bug in :func:`sdl2.ext.get_events()`, which did not handle
  more than 10 events in the queue correctly
* issue #8: :meth:`sdl2.ext.SpriteFactory.create_texture_sprite` can
  create sprites to be used as rendering targets now
* issue #9: improved error messages on trying to bind non-existent library
  functions via ctypes
* minor documentation fixes

Thanks to Steven Johnson, Todd Rovito, Bil Bas and Dan McCombs for
providing fixes and improvements.


0.4.0
-----
Released on 2013-06-08.

* new :mod:`sdl2.sdlmixer` module, which provides access to the
  SDL2_mixer library
* issue #1: fixed libc loading for cases where libc.so is a ld script
* updated :mod:`sdl2` and :mod:`sdl2.sdlimage` to include the latest
  changes of the libraries, they wrap

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
