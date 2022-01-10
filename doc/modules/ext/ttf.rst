.. currentmodule:: sdl2.ext

Text rendering routines
=======================

.. class:: FontManager(font_path : str[, alias=None[, size=16[, color=Color(255, 255, 255)[, bg_color=Color(0, 0, 0)[, index=0]]]]])

   Manage fonts and rendering of text.

   One font path must be given to initialise the FontManager.
   :attr:`default_font` will be set to this font. *size* is the default
   font size in pixels. *color* and *bg_color* will give the FontManager
   a default color. *index* will select a specific font face from a file
   containing multiple font faces. The first face is always at index 0. It can
   be used for TTC (TrueType Font Collection) fonts.

   .. attribute:: bg_color

      The :class:`sdl2.ext.Color` to be used as background color.

   .. attribute:: color

      The :class:`sdl2.ext.Color` to be used for rendering text.

   .. attribute:: default_font

      Returns the name of the current default font being used by the
      :class:`FontManager`. On assigning :attr:`default_font`,
      the value must be a loaded font alias.

   .. attribute:: size

      The default font size in pixels.

   .. method:: add(font_path : str[, alias=None[, size=None[, index=0]]])) -> sdl2.sdlttf.TTF_Font

      Add a font to the :class:`FontManager`. *alias* is by default the
      font name, any other name can be passed, *size* is the font size
      in pixels and defaults to :attr:`size`. *index* selects a specific font
      face from a TTC (TrueType Font Collection) file. Returns the font pointer
      stored in :attr:`fonts`.

   .. method:: close()

      Closes all fonts used by the :class:`FontManager`.

   .. method:: render(text : str[, alias=None[, size=None[, width=None[, color=None[, bg_color=None[, **kwargs]]]]]]) -> sdl2.SDL_Surface

      Renders text to a surface. This method uses the font designated by
      the passed *alias* or, if *alias* is omitted, by the set
      :attr:`default_font`.  A *size* can be passed even if the font was
      not loaded with this size.  A *width* can be given for automatic line
      wrapping.  If no *bg_color* or *color* are given, it will default to
      the FontManager's :attr:`bg_color` and :attr:`color`.
