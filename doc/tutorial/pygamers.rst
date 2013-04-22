PySDL2 for Pygamers
===================

Care to move to a newer SDL with your Pygame knowledge? Then you should
know one thing or two about PySDL2 before hacking code, since it is
completely different from Pygame. Do not let that fact scare you away,
the basics with graphics and sound are still the same (as they are
fundamental), but you will not find many similarities to the Pygame API
within PySDL2.

.. todo::

   More details, examples, etc.

Conceptual differences
----------------------
TODO

Technical differences
---------------------
Pygame is implemented as a mixture of Python, C and Assembler code,
wrapping 3rd party libraries with CPython API interfaces. PySDL2 in
contrast is written in pure Python, using :mod:`ctypes` to interface
with the C interfaces of 3rd party libraries.


API differences
---------------

pygame
^^^^^^
======================= =================================================
pygame                  sdl2
======================= =================================================
``init()``              :func:`sdl2.init()` where appropriate
``quit()``              :func:`sdl2.quit()` where appropriate
``error``               No equivalent
``get_error()``         :func:`sdl2.get_error()`
``set_error()``         :func:`sdl2.set_error()`
``get_sdl_version()``   :func:`sdl2.version.get_version()`
``get_sdl_byteorder()`` :data:`sdl2.endian.SDL_BYTEORDER`
``register_quit()``     No equivalent planned
``encode_string()``     Encoding and decoding strings is done implicitly,
                        where necessary
``encode_file_path()``  Encoding and decoding strings is done implicitly,
                        where necessary
======================= =================================================

pygame.cdrom
^^^^^^^^^^^^
PySDL2 does not feature any CD-ROM related interfaces. They were
removed in SDL2 and mule does not provide its own facilities.

pygame.Color
^^^^^^^^^^^^
You can find a similar class in :class:`sdl2.ext.color.Color`. It does
not feature a ``set_length()`` or ``correct_gamma()`` method, though.

pygame.cursors
^^^^^^^^^^^^^^
PySDL2 does not feature any pre-defined cursor settings at the moment.

pygame.display
^^^^^^^^^^^^^^
======================= =================================================
pygame.display          sdl2
======================= =================================================
``init()``              :func:`sdl2.ext.init()`
``quit()``              :func:`sdl2.ext.quit()`
``get_init()``          :func:`sdl2.SDL_WasInit()`
``set_mode()``          :class:`mule.video.window.Window`
``get_surface()``       :meth:`mule.video.window.Window.get_surface()`
``flip()``              :meth:`mule.video.window.Window.refresh()`
``update()``            :meth:`mule.sdl2.video.update_window_surface_rects()`
``get_driver()``        :func:`mule.sdl2.video.get_current_video_driver()`
``Info``                No equivalent yet
``get_wm_info()``       :func:`mule.sdl2.syswm.get_window_wm_info()`
``list_modes()``        :func:`mule.sdl2.video.get_num_display_modes()`
``mode_ok()``           :func:`mule.sdl2.video.get_closest_display_mode()`
``gl_get_attribute()``  :func:`mule.sdl2.video.gl_get_attribute()`
``gl_set_attribute()``  :func:`mule.sdl2.video.gl_set_attribute()`
``get_active()``        No equivalent yet
``iconify()``           :meth:`mule.video.window.Window.minimize()`
``toggle_fullscreen()`` :func:`mule.sdl2.video.set_window_fullscreen()`
``set_gamma()``         :func:`mule.sdl2.video.set_window_brightness()`
``set_gamma_ramp()``    :func:`mule.sdl2.video.set_window_gamma_ramp()`
``set_icon()``          :func:`mule.sdl2.video.set_window_icon()`
``set_caption()``       :attr:`mule.video.window.Window.title`
``get_caption()``       :attr:`mule.video.window.Window.title`
``set_palette()``       :func:`mule.sdl2.surface.set_surface_palette()`
======================= =================================================

pygame.draw
^^^^^^^^^^^
============== =================================================
pygame.draw    mule
============== =================================================
``rect()``     :func:`mule.sdl2.render.render_draw_rect()`,
               :func:`mule.video.draw.fill()`
``polygon()``  No equivalent yet
``circle()``   No equivalent yet
``ellipse()``  No equivalent yet
``arc()``      No equivalent yet
``lines()``    :func:`mule.sdl2.render.render_draw_lines()`,
               :func:`mule.video.draw.line()`
``aaline()``   No equivalent yet
``aalines()``  No equivalent yet
============== =================================================

pygame.event
^^^^^^^^^^^^
================= =================================================
pygame.event      mule
================= =================================================
``pump()``        :func:`mule.sdl2.events.pump_events()`
``get()``         :func:`mule.sdl2.events.poll_event()`
``poll()``        :func:`mule.sdl2.events.poll_event()`
``wait()``        :func:`mule.sdl2.events.wait_event()`
``peek()``        :func:`mule.sdl2.events.peep_events()`
``clear()``       :func:`mule.sdl2.events.flush_events()`
``event_name()``  No equivalent planned
``set_blocked()`` :func:`mule.sdl2.events.event_state()`
``get_blocked()`` :func:`mule.sdl2.events.event_state()`
``set_allowed()`` :func:`mule.sdl2.events.event_state()`
``set_grab()``    :func:`mule.sdl2.video.set_window_grab()`
``get_grab()``    :func:`mule.sdl2.video.get_window_grab()`
``post()``        :func:`mule.sdl2.events.peep_events()`
``Event``         :class:`mule.sdl2.events.SDL_Event`
================= =================================================

pygame.font
^^^^^^^^^^^
====================== =================================================
pygame.font            mule
====================== =================================================
``init()``             :func:`mule.sdlttf.init()`
``quit()``             :func:`mule.sdlttf.quit()`
``get_init()``         No equivalent planned
``get_default_font()`` No equivalent planned
``get_fonts()``        :func:`mule.font.get_fonts()`
``match_font()``       :func:`mule.font.get_font()`
``SysFont``            No equivalent planned
``Font``               No equivalent yet
====================== =================================================

pygame.freetype
^^^^^^^^^^^^^^^
mule does not feature direct FreeType support at the moment.

pygame.gfxdraw
^^^^^^^^^^^^^^
mule does not feature SDL_gfx support at the moment.

pygame.image
^^^^^^^^^^^^
================== =================================================
pygame.image       mule
================== =================================================
``load()``         :func:`mule.sdlimage.load()`,
                   :func:`mule.video.image.load_image()`
``save()``         :func:`mule.sdl2.surface.save_bmp()`
``get_extended()`` :func:`mule.sdlimage.is_bmp()` et al.
``tostring()``     No equivalent yet
``fromstring()``   No equivalent yet
``frombuffer()``   No equivalent yet
================== =================================================

pygame.joystick
^^^^^^^^^^^^^^^
================== ========================================================
pygame.joystick    mule
================== ========================================================
``init()``         :func:`mule.sdl2.init()`
``quit()``         :func:`mule.sdl2.quit()`
``get_init()``     :func:`mule.sdl2.was_init()`
``get_count()``    :func:`mule.sdl2.joystick.joystick_num_joysticks()`
``Joystick()``     :class:`mule.sdl2.joystick.SDL_Joystick` and related
                   functions
================== ========================================================

pygame.key
^^^^^^^^^^
================== ========================================================
pygame.key         mule
================== ========================================================
``get_focused()``  :func:`mule.sdl2.keyboard.get_keyboard_focus()`
``get_pressed()``  :func:`mule.sdl2.keyboard.get_keyboard_state()`
``get_mods()``     :func:`mule.sdl2.keyboard.get_mod_state()`
``set_mods()``     :func:`mule.sdl2.keyboard.set_mod_state()`
``set_repeat()``   Based on the OS/WM settings, no equivalent
``get_repeat()``   Based on the OS/WM settings, no equivalent
``name()``         :func:`mule.sdl2.keyboard.get_key_name()`
================== ========================================================

pygame.locals
^^^^^^^^^^^^^
Constants in mule are spread across the different packages and
modules, depending on where they originate from.

pygame.mixer
^^^^^^^^^^^^
SDL_mixer is currently not supported by mule. The focus is set on
OpenAL usage through :mod:`mule.openal` and :mod:`mule.audio`.

====================== ====================================================
pygame.mixer           mule
====================== ====================================================
``init()``             No necessity to explicitly initialize
``quit()``             No necessity to explicitly quit
``get_init()``         No necessity to explicitly initialize
``stop()``             ``mule.audio.SoundSource.request = SOURCE_STOP``
``pause()``            ``mule.audio.SoundSource.request = SOURCE_PAUSE``
``unpause()``          ``mule.audio.SoundSource.request = SOURCE_PLAY``
``fadeout()``          No equivalent yet
``set_num_channels()`` Depends on the :class:`mule.audio.SoundSink`
                       device and bound
                       :class:`mule.audio.SoundSource` instances.
``get_num_channels()`` Depends on the :class:`mule.audio.SoundSink`
                       device and bound
                       :class:`mule.audio.SoundSource` instances.
``set_reserved()``     Depends on the :class:`mule.audio.SoundSink`
                       device and bound
                       :class:`mule.audio.SoundSource` instances.
``find_channel()``     No equivalent planned
``get_busy()``         No equivalent yet
``Sound``              :class:`mule.audio.SoundData` for the buffer,
                       :class:`mule.audio.SoundSource` for the volume
                       settings and playback
``Channel``            :class:`mule.audio.SoundSource`
====================== ====================================================

pygame.mixer.music
^^^^^^^^^^^^^^^^^^
See `pygame.mixer`_.


pygame.mouse
^^^^^^^^^^^^
================= ====================================================
pygame.mouse      mule
================= ====================================================
``get_pressed()`` :func:`mule.sdl2.mouse.get_mouse_state()`
``get_pos()``     :func:`mule.sdl2.mouse.get_mouse_state()`
``get_rel()``     :func:`mule.sdl2.mouse.get_relative_mouse_state()`
``set_pos()``     :func:`mule.sdl2.mouse.warp_mouse_in_window()`
``set_visible()`` :func:`mule.sdl2.mouse.show_cursor()`
``get_focused()`` :func:`mule.sdl2.mouse.get_mouse_focus()`
``set_cursor()``  :func:`mule.sdl2.mouse.set_cursor()`
``get_cursor()``  :func:`mule.sdl2.mouse.get_cursor()`
================= ====================================================

pygame.movie
^^^^^^^^^^^^
No such module is planned for mule.

pygame.Overlay
^^^^^^^^^^^^^^
You can work with YUV overlays by using the :mod:`mule.sdl2.render`
with :class:`mule.sdl2.render.SDL_Texture` objects.

pygame.PixelArray
^^^^^^^^^^^^^^^^^
You can access pixel data of sprites and surfaces directly via the
:class:`mule.video.pixelaccess.PixelView` class. It does not feature
comparision or extractions methods.

pygame.Rect
^^^^^^^^^^^
No such functionality is available for mule. Rectangles are represented
via :class:`mule.sdl2.rect.SDL_Rect` for low-level SDL2 wrappers or 4-value
tuples.

pygame.scrap
^^^^^^^^^^^^
mule offers basic text-based clipboard access via the
:mod:`mule.sdl2.clipboard` module. A feature-rich clipboard API as for
Pygame does not exist yet.

pygame.sndarray
^^^^^^^^^^^^^^^
No such module is available for mule yet.

pygame.sprite
^^^^^^^^^^^^^
mule uses a different approach of rendering and managing sprite
objects via a component-based system and the
:class:`mule.video.sprite.Sprite` class. A sprite module as for Pygame is
not planned.

pygame.Surface
^^^^^^^^^^^^^^
======================= =====================================================
pygame.Surface          mule
======================= =====================================================
``blit()``              :meth:`mule.video.sprite.SpriteRenderer.render()`,
                        :func:`mule.sdl2.surface.blit_surface()`
``convert()``           :func:`mule.sdl2.surface.convert_surface()`
``convert_alpha()``     :func:`mule.sdl2.surface.convert_surface()`
``copy()``              :func:`mule.sdl2.surface.convert_surface()`
``fill()``              :func:`mule.video.draw.fill()`,
                        :func:`mule.sdl2.surface.fill_rect()`,
                        :func:`mule.sdl2.surface.fill_rects()`
``scroll()``            No equivalent yet
``set_colorkey()``      :func:`mule.sdl2.surface.set_color_key()`
``get_colorkey()``      :func:`mule.sdl2.surface.get_color_key()`
``set_alpha()``         :func:`mule.sdl2.surface.set_surface_alpha_mod()`
``get_alpha()``         :func:`mule.sdl2.surface.get_surface_alpha_mod()`
``lock()``              :func:`mule.sdl2.surface.lock_surface()`
``unlock()``            :func:`mule.sdl2.surface.unlock_surface()`
``mustlock()``          :func:`mule.sdl2.surface.SDL_MUSTLOCK()`
``get_locked()``        :attr:`mule.sdl2.surface.SDL_Surface.locked`
``get_locks()``         No equivalent planned
``get_at()``            Direct access to the pixels for surfaces can be
                        achieved via the
                        :class:`mule.video.pixelaccess.PixelView` class
``set_at()``            Direct access to the pixels for surfaces can be
                        achieved via the
                        :class:`mule.video.pixelaccess.PixelView` class
``get_at_mapped()``     No equivalent planned
``get_palette()``       via :attr:`mule.sdl2.surface.SDL_Surface.format`
                        and the
                        :attr:`mule.sdl2.pixels.SDL_PixelFormat.palette`
                        attribute.
``get_palette_at()``    ``mule.sdl2.pixels.SDL_Palette.colors[offset]``
``set_palette()``       :func:`mule.sdl2.surface.set_surface_palette()`
``set_palette_at()``    ``mule.sdl2.pixels.SDL_Palette.colors[offset]``
``map_rgb()``           :func:`mule.sdl2.pixels.map_rgb()`
``unmap_rgb()``         :func:`mule.sdl2.pixels.get_rgb()`
``set_clip()``          :func:`mule.sdl2.surface.set_clip_rect()`
``get_clip()``          :func:`mule.sdl2.surface.get_clip_rect()`
``subsurface``          No equivalent yet
``get_parent()``        As for ``subsurface``
``get_abs_parent()``    As for ``subsurface``
``get_offset()``        As for ``subsurface``
``get_abs_offset()``    As for ``subsurface``
``get_size()``          :attr:`mule.video.sprite.Sprite.size`,
                        :attr:`mule.sdl2.surface.SDL_Surface.size`
``get_width()``         ``mule.video.sprite.Sprite.size[0]``,
                        ``mule.sdl2.surface.SDL_Surface.size[0]``
``get_height()``        ``mule.video.sprite.Sprite.size[1]``,
                        ``mule.sdl2.surface.SDL_Surface.size[1]``
``get_rect()``          :attr:`mule.video.sprite.Sprite.area`
``get_bitsize()``       :attr:`mule.sdl2.pixels.SDL_PixelFormat.BitsPerPixel`
``get_bytesize()``      :attr:`mule.sdl2.pixels.SDL_PixelFormat.BytesPerPixel`
``get_flags()``         :attr:`mule.sdl2.surface.SDL_Surface.flags`
``get_pitch()``         :attr:`mule.sdl2.surface.SDL_Surface.pitch`
``get_masks()``         :attr:`mule.sdl2.pixels.SDL_PixelFormat.Rmask`, ...
``get_shifts()``        :attr:`mule.sdl2.pixels.SDL_PixelFormat.Rshift`, ...
``get_losses()``        :attr:`mule.sdl2.pixels.SDL_PixelFormat.Rloss`, ...
``get_bounding_rect()`` No equivalent yet
``get_view()``          :class:`mule.video.pixelaccess.PixelView`
``get_buffer()``        :class:`mule.video.pixelaccess.PixelView` or
                        :attr:`mule.sdl2.surface.SDL_Surface.pixels`
======================= =====================================================

pygame.surfarray
^^^^^^^^^^^^^^^^
2D and 3D pixel access can be achieved via the
:class:`mule.video.pixelaccess.PixelView` class in environments without
numpy. Simplified numpy-array creation with direct pixel access (similar
to ``pygame.surfarray.pixels2d()`` and ``pygame.surfarray.pixels3d()``)
is available via :func:`mule.video.pixelaccess.pixels2d()` and
:func:`mule.video.pixelaccess.pixels3d()`.

pygame.time
^^^^^^^^^^^
=============== =================================================
pygame.time     mule
=============== =================================================
``get_ticks()`` :func:`mule.sdl2.timer.get_ticks()`
``wait()``      :func:`mule.sdl2.timer.delay()`
``delay()``     :func:`mule.sdl2.timer.delay()`
``Clock``       No equivalent yet
=============== =================================================

pygame.transform
^^^^^^^^^^^^^^^^
The are no transformation helpers in mule at moment. Those might be
implemented later on via numpy helpers, the Python Imaging Library or
other 3rd party packages.

pygame.version
^^^^^^^^^^^^^^
=============== =================================================
pygame.version  mule
=============== =================================================
``ver``         :attr:`mule.__version__`
``vernum``      :attr:`mule.version_info`
=============== =================================================
