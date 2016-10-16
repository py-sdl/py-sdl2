.. currentmodule:: sdl2.ext

Text rendering routines
=======================

.. class:: BitmapFont(surface : Sprite, size : iterable[, mapping=None)

   A bitmap graphics to character mapping. The :class:`BitmapFont` class
   uses an image *surface* to find and render font character glyphs for
   text. It requires a mapping table, which denotes the characters
   available on the image.

   The mapping table is a list of strings, where each string reflects a
   *line* of characters on the image. Each character within each line
   has the same size as specified by the size argument.

   A typical mapping table might look like ::

      [ '0123456789',
        'ABCDEFGHIJ',
        'KLMNOPQRST',
        'UVWXYZ    ',
        'abcdefghij',
        'klmnopqrst',
        'uvwxyz    ',
        ',;.:!?+-()' ]

   .. attribute:: surface

      The :class:`sdl2.SDL_Surface` containing the character bitmaps.

   .. attribute:: offsets

      A dict containing the character offsets on the :attr:`surface`.

   .. attribute:: mapping

      The character mapping table, a list of strings.

   .. attribute:: size

      The size of an individual glyph bitmap on the font.

   .. method:: render(text : string[, bpp=None]) -> Sprite

      Renders the passed text on a new :class:`Sprite` and returns it.
      If no explicit *bpp* are provided, the bpp settings of the
      :attr:`.surface` are used.

   .. method:: render_on(surface : Sprite, text : string[, \
                         offset=(0, 0)]) -> (int, int, int, int)

      Renders a text on the passed sprite, starting at a specific
      offset. The top-left start position of the text will be the
      passed *offset* and a 4-value tuple with the changed area will be
      returned.

   .. method:: contains(c : string) -> bool

      Checks, whether a certain character exists in the font.

   .. method:: can_render(text : string) -> bool

      Checks, whether all characters in the passed *text* can be rendered.

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
