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
