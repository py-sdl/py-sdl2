Release News
============
This describes the latest changes between the PySDL2 releases.

0.9.0
-----
Released on

**IMPORTANT: This release breaks backwards-compatibility. See the notes
for the issues #36 and #39.**

* updated :mod:`sdl2` to include the latest changes of SDL2 (release 2.0.3)
* new :func:`sdl2.ext.subsurface()` function to create subsurfaces from
  :class:`sdl2.SDL_Surface` objects
* new :func:`sdl2.ext.SoftwareSprite.subsprite()` method to create
  :class:`sdl2.ext.SoftwarSprite` objects sharing pixel data
* the unit test runner features a `--logfile` argument now to
  safe the unit test output to a file
* issues #36, #39: the different render classes of sdl2.ext.sprite were renamed
  
  * the ``sdl2.ext.RenderContext`` class was renamed to
    :class:`sdl2.ext.Renderer` to be consistent with with SDL2's naming scheme
  * ``sdl2.ext.SpriteRenderer`` was renamed to
    :class:`sdl2.ext.SpriteRenderSystem`
  * ``sdl2.ext.SoftwareSpriteRenderer`` was renamed to
    :class:`sdl2.ext.SoftwareSpriteRenderSystem`
  * ``sdl2.ext.TextureSpriteRenderer`` was renamed to
    :class:`sdl2.ext.TextureSpriteRenderSystem`
  * ``sdl2.ext.SpriteFactory.create_sprite_renderer()`` was renamed to
    :meth:`sdl2.ext.SpriteFactory.create_sprite_render_system()`

* fixed :func:`sdl2.audio.SDL_LoadWAV()` macro to provide the correct arguments
* fixed issue #44: use a slightly less confusing ``ValueError``, if a renderer
  argument for the :class:`sdl2.ext.SpriteFactory` is not provided
* fixed issue #43: improved the code reference for the improved bouncing
  section in the docs
* fixed issue #40: typo in a ``RuntimeWarning`` message on loading the SDL2
  libraries
* fixed issue #38: the points arguments of
  :meth:`sdl2.ext.Renderer.draw_points()` are properly documented now
* fixed issue #37: :func:`sdl2.SDL_GetRendererOutputSize()` is now acccessible
  via a wildcard import
* fixed issue #35: download location is now mentioned in the docs
* fixed issue #12: remove confusing try/except on import in the examples

  
0.8.0
-----
Released on 2013-12-30.

* updated PD information to include the CC0 dedication, since giving
  software away is not enough anymore
* updated :mod:`sdl2` to include the latest changes of SDL2 (HG)
* fixed a wrong C mapping of :func:`sdl2.rwops.SDL_FreeRW()`
* fixed various issues within the :class:`sdl2.ext.BitmapFont` class
* issue #26: :attr:`sdl2.SDL_AudioSpec.callback` is a :func:`SDL_AudioCallBack`
  now
* issue #30: the SDL_Add/DelHintCallback() unittest works with PyPy now
* issue #31: :func:`sdl2.sdlmixer.SDL_MIXER_VERSION()` returns the proper
  version now

Thanks to Sven Eckelmann, Marcel Rodrigues, Michael McCandless,
Andreas Schiefer and Franz Schrober for providing fixes and
improvements.

0.7.0
-----
Released on 2013-10-27.

* updated :mod:`sdl2` to include the latest changes of SDL2 (release 2.0.1)
* fixed a bug in :meth:`sdl2.ext.FontManager.render()`, which did not apply
  the text color correctly
* issue #14: improved the error messages on failing DLL imports
* issue #19: the :meth:`sdl2.ext.TextureSpriteRenderer.render()` and
  :meth:`sdl2.ext.SoftwareSpriteRenderer.render()` methods do not
  misinterpret x and y arguments anymore, if set to 0
* issue #21: :func:`sdl2.ext.load_image()` raises a proper
  :exc:`UnsupportedError`, if neither SDL_image nor PIL are usable

Thanks to Marcel Rodrigues, Roger Flores and otus for providing fixes
and improvement ideas.

0.6.0
-----
Released on 2013-09-01.

* new :attr:`sdl2.ext.FontManager.size` attribute, which gives a default size
  to be used for adding fonts or rendering text
* updated :mod:`sdl2` to include the latest changes of SDL2
* :meth:`sdl2.ext.RenderContext.copy()` accepts any 4-value sequence as source
  or destination rectangle now
* issue #11: throw an :exc:`ImportError` instead of a
  :exc:`RuntimeError`, if a third-party DLL could not be imported
  properly
* fixed a bug in the installation code, which caused :mod:`sdl2.examples` not
  to install the required resources

Thanks to Steven Johnson for his enhancements to the FontManager class.
Thanks to Marcel Rodrigues for the improvements to RenderContext.copy().

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
