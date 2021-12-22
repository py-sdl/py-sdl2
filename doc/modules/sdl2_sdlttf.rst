sdl2.sdlttf - Python bindings for SDL2_ttf
==========================================

py-sdl2 provides bindings for SDL2_ttf, a library designed for use with SDL2
that provides high quality TrueType font rendering.

The SDL2_ttf library provides functions for rendering three main formats of
text, denoted by the suffix of the function. Functions ending in ``Text`` can only
render plain ASCII text, whereas functions ending in ``UTF8`` or ``UNICODE`` can
render most unicode characters provided that a font supports them. The `UNICODE`
functions are more-or-less useless in the context of Python, since it's much
easier and more stable across platforms and versions to convert Python strings
to utf-8 bytestrings than it is to convert them to ctypes arrays of UCS-2
characters, and the `UNICODE` functions convert their input to utf-8 before
rendering anyway so there's no functionality or character support lost by using
their `UTF8` counterparts.

SDL2_ttf supports a range of input formats, including TrueType (.ttf) and
OpenType (.otf) fonts. It also supports different font styles, font hinting
modes, and font outlines.

.. note::
   This module handles font sizes in units of points (pt) instead of pixels. To
   obtain a font with a given pixel height, you can use the
   :func:`TTF_GlyphMetrics` function to get the pixel heights of different
   glyphs in the font at a given pt size and use the px/pt ratio to figure out
   the pt size needed to render text at a given height in px.


Initialization functions
------------------------

.. function:: TTF_Init()

   Initializes the TTF engine.
   
   This must be called before using other functions in this library, except
   :func:`TTF_WasInit`. SDL does not have to be initialized before this call. 
   
   :returns: 0 if successful, -1 on error
   :rtype: int


.. function:: TTF_Quit()
   
   De-initialize the TTF engine.
   
   Other SDL_ttf functions should not be used after calling this, except for
   :func:`TTF_WasInit`, until :func:`TTF_Init` is called to re-initialize
   the engine.
  

.. function:: TTF_WasInit()

   Check if the TTF engine is initialized.
   
   You may use this before :func:`TTF_Init` to avoid initializing twice
   in a row, or to determine if you need to call :func:`TTF_Quit`.

   :returns: 1 if already initialized, 0 if not initialized.
   :rtype: int


.. function:: TTF_OpenFont(file, ptsize)

   Opens a given font file, creating a font object from it at the specified
   size.

   Point size is based on 72 DPI. File paths can be relative or absolute.

   .. code-block:: python

      fontpath = sdl2.ext.byteify(os.path.join('path', 'to', 'font.ttf'))
      font = TTF_OpenFont(fontpath, 23)
   
   :param file: A UTF8-encoded bytestring containing the path to the font
     file to load.
   :type file: bytes
   :param ptsize: The size in points (pt) at which to open the font.
   :type ptsize: int
   
   :rtype: POINTER(:obj:`TTF_Font`)


.. function:: TTF_OpenFontIndex(file, ptsize, index)

   Opens a specific font face by index number from a given multi-face font file,
   creating a font object from it at the specified size.

   Point size is based on 72 DPI. File paths can be relative or absolute.

   .. code-block:: python

      fontpath = sdl2.ext.byteify(os.path.join('path', 'to', 'font.ttf'))
      font = TTF_OpenFontIndex(fontpath, 23, 2)
   
   :param file: A UTF8-encoded bytestring containing the path to the font
     file to load.
   :type file: bytes
   :param ptsize: The size in points (pt) at which to open the font.
   :type ptsize: int
   :param index: The index of the font face to open. Must be a number from
     1 to 255.
   :type index: int
   
   :rtype: POINTER(:obj:`TTF_Font`)


.. function:: TTF_OpenFontRW(src, freesrc, ptsize)

   Opens a font from an :obj:`SDL_RWops` file object, creating a font object
   from it at the specified size.

   Point size is based on 72 DPI.

   .. note::
      The SDL2 RW object used to create the font (``src``) must be kept in
      memory until you are done with the font. Once the ``src`` has been freed,
      performing any operations with the returned :obj:`TTF_Font` will result in
      a segfault.
   
   :param src: An ``SDL_RWops`` file object containing a valid font.
   :type src: POINTER(SDL_RWops)
   :param freesrc: If non-zero, the provided file object will be closed and
     freed automatically when the resulting :obj:`TTF_Font` is closed (or if
     an error is encountered opening the font).
   :type freesrc: int
   :param ptsize: The size in points (pt) at which to open the font.
   :type ptsize: int
   
   :rtype: POINTER(:obj:`TTF_Font`)


.. function:: TTF_OpenFontIndexRW(src, freesrc, ptsize, index)

   Opens a specific font face by index number from an :obj:`SDL_RWops` file
   object containing a multi-face font, creating a font object from it at the
   specified size.

   Point size is based on 72 DPI.

   .. note::
      The SDL2 RW object used to create the font (``src``) must be kept in
      memory until you are done with the font. Once the ``src`` has been freed,
      performing any operations with the returned :obj:`TTF_Font` will result in
      a segfault.
   
   :param src: An ``SDL_RWops`` file object containing a valid font.
   :type src: POINTER(SDL_RWops)
   :param freesrc: If non-zero, the provided file object will be closed and
     freed automatically when the resulting :obj:`TTF_Font` is closed (or if
     an error is encountered opening the font).
   :type freesrc: int
   :param ptsize: The size in points (pt) at which to open the font.
   :type ptsize: int
   :param index: The index of the font face to open. Must be a number from
     1 to 255.
   :type index: int
   
   :rtype: POINTER(:obj:`TTF_Font`)


.. function:: TTF_CloseFont(font)
    
   Frees the memory used by a given font, once you are done with it.
   The font cannot be used after this.
   
   :param font: A pointer to the font to close.
   :type font: POINTER(:obj:`TTF_Font`)


.. function:: TTF_ByteSwappedUNICODE(swapped)

   Tells the library whether UNICODE text is generally byteswapped.
   
   A UNICODE BOM character in a string will override this setting for the
   remainder of that string. The default mode is non-swapped, native
   endianness of the CPU. 

   Note that this only affects the behaviour of UNICODE (UCS-2)
   functions and not UTF8 functions.
   
   :param swapped: If 0, native CPU endianness will be used. If not 0,
     UNICODE data will be byte-swapped relative to native CPU endianness. 
   :type swapped: int


.. function:: TTF_Linked_Version()

   This function gets the version of the dynamically linked SDL2_ttf library.   
   
   :returns: a pointer to an object containing the version of the SDL2_ttf
     library currently in use.
   :rtype: POINTER(:obj:`SDL_version`)



Font attribute functions
------------------------

.. function:: TTF_SetFontStyle(font, style)

   Sets the style for a given font, as specified using the following
   constants:

   ============= ===========================
   Style         Constant
   ============= ===========================
   Normal        ``TTF_STYLE_NORMAL``
   Bold          ``TTF_STYLE_BOLD``
   Italics       ``TTF_STYLE_ITALICS``
   Underlined    ``TTF_STYLE_UNDERLINE``
   Strikethrough ``TTF_STYLE_STRIKETHROUGH``
   ============= ===========================

   Multiple font styles (e.g. bold and italics) can be combined using the
   bitwise ``|`` operator.

   .. code-block:: python

     underlined_bold = (TTF_STYLE_BOLD | TTF_STYLE_UNDERLINE)
     TTF_SetFontStyle(font, underlined_bold)

   .. note::
      Setting the underline style for a font may cause the surfaces created by
      :obj:`TTF_RenderGlyph` functions to be taller, in order to make room for
      the underline to be drawn underneath.
   
   :param font: The loaded font for which the style should be set.
   :type font: POINTER(:obj:`TTF_Font`)
   :param style: A bitmask specifying the new style to use for the font.
   :type style: int


.. function:: TTF_GetFontStyle(font)

   Retrieves the rendering style of a given font. Returns one of the constants
   specified in the documentation for :func:`TTF_SetFontStyle`.

   :param font: The loaded font to get the current style of.
   :type font: POINTER(:obj:`TTF_Font`)
   
   :rtype: int
   

.. function:: TTF_SetFontOutline(font, outline)

   Sets the outline thickness (in pixels) for a given font.

   If the outline is set to zero, outlining will be disabled for the font.
   
   :param font: The loaded font to set the outline thickness for.
   :type font: POINTER(:obj:`TTF_Font`)
   :param outline: The new outline thickness to use for the font.
   :type outline: int
   
   
.. function:: TTF_GetFontOutline(font)

   Retrieves the outline thickness (in pixels) of a given font.
   
   :param font: The loaded font to get the current outline thickness of.
   :type font: POINTER(:obj:`TTF_Font`)
   
   :rtype: int


.. function:: TTF_SetFontHinting(font, hinting)

   Sets the hinting mode for a given font, as specified using one of the
   following constants:

   ============= =======================
   Hinting type  Constant
   ============= =======================
   Normal        ``TTF_HINTING_NORMAL``
   Light         ``TTF_HINTING_LIGHT``
   Mono          ``TTF_HINTING_MONO``
   None          ``TTF_HINTING_NONE``
   ============= =======================

   If no hinting mode is is explicitly set, "normal" hinting is used for
   rendering.
   
   :param font: The loaded font to set the hinting mode setting for.
   :type font: POINTER(:obj:`TTF_Font`)
   :param hinting: A constant specifying the type of hinting to use when
     rendering the font.
   :type hinting: int
   

.. function:: TTF_GetFontHinting(font)

   Retrieves the current hinting setting of a given font. Returns one of the
   constants specified in the documentation for :func:`TTF_SetFontHinting`.
   
   :param font: The loaded font to get the current hinting mode of.
   :type font: POINTER(:obj:`TTF_Font`)
   
   :rtype: int


.. function:: TTF_FontHeight(font)

   Get the maximum pixel height of all glyphs of a given font. This is
   usually equal to point size.

   You can use this height for rendering text as close together vertically
   as possible, though adding at least one pixel height to it will space it
   so they can't touch.
   
   :param font: The loaded font to get the maximum height of. 
   :type font: POINTER(:obj:`TTF_Font`)
   
   :returns: The maximum pixel height of all glyphs in the font.
   :rtype: int


.. function:: TTF_FontAscent(font)

   Get the maximum pixel ascent of all glyphs of a given font. This can
   also be interpreted as the distance from the top of the font to the
   baseline.
   
   :param font: The loaded font to get the ascent (height above baseline) of.
   :type font: POINTER(:obj:`TTF_Font`)
   
   :returns: A positive value in pixels, relative to the baseline.
   :rtype: int


.. function:: TTF_FontDescent(font)

   Get the maximum pixel descent of all glyphs of a given font. This can
   also be interpreted as the distance from the baseline to the bottom of
   the font.
   
   :param font: The loaded font to get the descent (height below baseline) of.
   :type font: POINTER(:obj:`TTF_Font`)
   
   :returns: A negative value in pixels, relative to the baseline.
   :rtype: int


.. function:: TTF_FontLineSkip(font)

   Gets the recommended spacing between lines of text for a given font.
   This is usually larger than the result of :func:`TTF_FontHeight`.
   
   :param font: The loaded font to get the suggested line skip height for.
   :type font: POINTER(:obj:`TTF_Font`)
   
   :returns: The recommended height (in pixels) for each line of text.
   :rtype: int


.. function:: TTF_GetFontKerning(font)

   Gets whether or not kerning is enabled for a given font.
   
   :param font: The loaded font to get the kerning status of.
   :type font: POINTER(:obj:`TTF_Font`)
   
   :returns: 0 if kerning disabled, non-zero if kerning enabled.
   :rtype: int


.. function:: TTF_SetFontKerning(font, allowed)

   Enables or disables font kerning for a given font. Kerning is enabled
   for all fonts by default.
   
   :param font: The loaded font to enable or disable kerning for.
   :type font: POINTER(:obj:`TTF_Font`)
   :param allowed: 0 to disable kerning, non-zero to allow it.
   :type allowed: int
   

.. function:: TTF_FontFaces(font)

   Get the number of faces ("sub-fonts") available in a given font.
   
   This is a count of the number of specific fonts (based on size and style
   and other typographical features) contained in the font itself.
   
   :param font: The loaded font to get the number of available faces from. 
   :type font: POINTER(:obj:`TTF_Font`)
   
   :returns: The number of faces in the font.
   :rtype: int


.. function:: TTF_FontFaceIsFixedWidth(font)

   Test if the current font face of a given font is fixed width.

   Fixed width fonts are monospace, meaning every character that exists in the
   font is the same width, thus you can assume that a rendered string's width
   is going to be the result of a simple calculation:
   ``glyph_width * string_length``.
   
   :param font: The loaded font to get the fixed width status of. 
   :type font: POINTER(:obj:`TTF_Font`)
   
   :returns: An int greater than 0 if the font is fixed width, otherwise 0.
   :rtype: int


.. function:: TTF_FontFaceFamilyName(font)

   Gets the current font face family name from a given font.
   
   :param font: The loaded font to get the current face family name of.
   :type font: POINTER(:obj:`TTF_Font`)

   :returns: The name of the current family of the given font, or ``None``
     if not available.
   :rtype: bytes


.. function:: TTF_FontFaceStyleName(font)

   Gets the current font face style name from a given font.
   
   :param font: The loaded font to get the current face style of.
   :type font: POINTER(:obj:`TTF_Font`)
   
   :returns: The name of the current style name of the given font, or ``None``
     if not available.
   :rtype: bytes


.. function:: TTF_GlyphIsProvided(font, ch)

   Checks whether a glyph is provided by a given font.
   
   :param font: The loaded font to get the glyph availability in.
   :type font: POINTER(:obj:`TTF_Font`)
   :param ch: The UNICODE (UCS-2) integer of the glyph to test availability of.
   :type ch: int
   
   :rtype: int


.. function:: TTF_GlyphMetrics(font, ch, minx, maxx, miny, maxy, advance)

   Gets the metrics (dimensions) of a glyph for a given font.

   .. code-block:: python

     from ctypes import c_int, byref

     minX, maxX, minY, maxY = c_int(0), c_int(0), c_int(0), c_int(0)
     adv = c_int(0)
     TTF_GlyphMetrics(
         font, ord(char),
         byref(minX), byref(maxX), byref(minY), byref(maxY), byref(adv)
     )
     results = [x.value for x in (minX, maxX, minY, maxY, adv)]

   To understand what these metrics mean, here is a useful link:
   http://freetype.sourceforge.net/freetype2/docs/tutorial/step2.html
   
   :param font: The loaded font from which to get the glyph metrics of ch.
   :type font: POINTER(:obj:`TTF_Font`)
   :param ch: The UNICODE (UCS-2) integer of the glyph to get metrics for.
   :type ch: int
   :param minx: Integer pointer in which to store the glyph's minimum X offset.
   :type minx: POINTER(:obj:`ctypes.c_int`)
   :param maxx: Integer pointer in which to store the glyph's maximum X offset.
   :type maxx: POINTER(:obj:`ctypes.c_int`)
   :param miny: Integer pointer in which to store the glyph's minimum Y offset.
   :type miny: POINTER(:obj:`ctypes.c_int`)
   :param maxy: Integer pointer in which to store the glyph's maximum Y offset.
   :type maxy: POINTER(:obj:`ctypes.c_int`)
   :param advance: Integer pointer in which to store the glyph's advance offset.
   :type advance: POINTER(:obj:`ctypes.c_int`)
   
   :returns: 0 on success, with all parameters set to the glyph metric as
     appropriate. -1 on errors, e.g. when the named glyph does not exist in
     the font. 
   :rtype: int


.. function:: TTF_GetFontKerningSizeGlyphs(font, previous_ch, ch)
   
   Gets the kerning size of two glyphs (by FreeType index) for a given font.

   .. note::
      The units of the return type of this function are undocumented in
      SDL_ttf. If you figure out what they are, please let us know!

   :param font: A pointer to the font to get the kerning size for.
   :type font: POINTER(:obj:`TTF_Font`)
   :param previous_ch: The UNICODE (UCS-2) integer of the first glyph.
   :type previous_ch: int
   :param ch: The UNICODE (UCS-2) integer of the second glyph.
   :type ch: int



Font rendering functions
------------------------

.. function:: TTF_SizeText(font, text, w, h)

   Calculates the resulting surface size of an ASCII-encoded string rendered
   using a given font. No actual rendering is done, but correct kerning is
   performed to get the actual width. The height returned in ``h`` is the same
   as that returned by :func:`TTF_FontHeight`. 
   
   :param font: The loaded font to use for surface size calculations.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: The ASCII string to determine the surface size of.
   :type text: bytes
   :param w: Integer pointer in which to store the surface width in pixels.
   :type w: POINTER(:obj:`ctypes.c_int`)
   :param h: Integer pointer in which to store the surface height in pixels.
   :type h: POINTER(:obj:`ctypes.c_int`)
   
   :returns: 0 if successful, -1 on error (e.g. if a glyph is not found in
     the provided font)
   :rtype: int


.. function:: TTF_SizeUTF8(font, text, w, h)

   Calculates the resulting surface size of a UTF-8 encoded string rendered
   using a given font. See :func:`TTF_SizeText` for more info.
   
   :param font: The loaded font to use for surface size calculations.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: The UTF-8 encoded string to determine the surface size of.
   :type text: bytes
   :param w: Integer pointer in which to store the surface width in pixels.
   :type w: POINTER(:obj:`ctypes.c_int`)
   :param h: Integer pointer in which to store the surface height in pixels.
   :type h: POINTER(:obj:`ctypes.c_int`)
   
   :returns: 0 if successful, -1 on error (e.g. if a glyph is not found in
     the provided font)
   :rtype: int


.. function:: TTF_SizeUNICODE(font, text, w, h)
   
   Calculates the resulting surface size of a UCS-2 encoded string rendered
   using a given font.
   
   See :func:`TTF_SizeText` and :func:`TTF_RenderUNICODE_Solid` for more info.
   
   :param font: The loaded font to use for surface size calculations.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: A ctypes uint16 array containing the glyphs of the UCS-2 string
     for which the rendered surface size should be calculated.
   :type text: POINTER(Uint16)
   :param w: Integer pointer in which to store the surface width in pixels.
   :type w: POINTER(:obj:`ctypes.c_int`)
   :param h: Integer pointer in which to store the surface height in pixels.
   :type h: POINTER(:obj:`ctypes.c_int`)
   
   :returns: 0 if successful, -1 on error (e.g. if a glyph is not found in
     the provided font)
   :rtype: int


.. function:: TTF_RenderText_Solid(font, text, fg)

   Renders a string of ASCII encoded text to a new 8-bit palettized surface
   with a transparent background and no antialiasing, using the given font
   and color.
   
   The 0 pixel is the colorkey, giving a transparent background, and the 1
   pixel is set to the text color. This allows you to change the color without
   having to render the text again. Palette index 0 is not drawn when the
   returned surface is blitted to another surface, since it is the colorkey
   and thus transparent, though its actual color is 255 minus each of the RGB
   components of the foreground color.
   
   This is the fastest of all the text rendering types. The resulting surface
   has a transparent background unlike :func:`TTF_RenderText_Shaded`, but the
   rendered text is not antialised and will thus appear pixelated and difficult
   to read at small sizes. The resulting surface should blit faster than the
   one returned by :func:`TTF_RenderText_Blended`. This rendering type should
   be used in cases when you need to render lots of text very quickly (e.g. if
   you're updating it every frame) or when you don't care about antialiasing.
  
   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: The ASCII string to render.
   :type text: bytes
   :param fg: The color to render the text in. This becomes colormap index 1.
   :type fg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderUTF8_Solid(font, text, fg)

   Renders a string of UTF-8 encoded text to a new 8-bit palettized surface
   with a transparent background and no antialiasing, using the given font
   and color. See :func:`TTF_RenderText_Solid` for more info.
   
   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: The UTF-8 string to render.
   :type text: bytes
   :param fg: The color to render the text in. This becomes colormap index 1.
   :type fg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderUNICODE_Solid(font, text, fg)
   
   Renders a string of UCS-2 encoded text to a new 8-bit palettized surface
   with a transparent background and no antialiasing, using the given font
   and color. See :func:`TTF_RenderText_Solid` for more info.

   The required text input format for this function is a ctypes array of
   UNICODE (UCS-2) glyphs in uint16 format, optionally terminated by a
   byte-order mark (``UNICODE_BOM_NATIVE`` or ``UNICODE_BOM_SWAPPED``)
   indicating how the text should be interpreted. Python strings can be
   converted to this format using the following code:

   .. code-block:: python

      # Generate UCS-2 array from Python string
      teststr = u"Hello world!"
      strlen = len(teststr + 1) # +1 for byte-order mark
      intstr = unpack('H' * strlen, teststr.encode('utf-16'))
      strarr = (ctypes.c_uint16 * strlen)(*intstr)

      # Render UCS-2 string
      col = SDL_Color(0, 0, 0)
      rendered = TTF_RenderUNICODE_Solid(font, strarr, col)

   Unless there is a very specific need, the ``TTF_RenderUTF8`` functions should
   always be used instead of their ``TTF_RenderUNICODE`` counterparts. In
   addition to having a much friendlier Python API and being more stable (see
   below), SDL_ttf uses the ``TTF_RenderUTF8`` functions internally for all the
   ``TTF_RenderUNICODE`` functions anyway so there is no benefit in terms of
   supporting a wider range of characters.

   .. note::
      The exact surface size generated by this and other UNICODE rendering
      functions varies seemingly at random on certain platforms and Python
      versions, even when provided the exact same array of integers as input.
      The Text and UTF8 rendering functions do not share this instability.
   
   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: A ctypes uint16 array containing the glyphs of the UCS-2 string
     to render.
   :type text: POINTER(Uint16)
   :param fg: The color to render the text in. This becomes colormap index 1.
   :type fg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderGlyph_Solid(font, ch, fg)

   Renders a single UNICODE (UCS-2) glyph to a new 8-bit palettized surface
   with a transparent background and no antialiasing, using the given font
   and color.

   The 0 pixel is the colorkey, giving a transparent background, and the 1
   pixel is set to the text color. The glyph is rendered without any padding
   or centering in the X direction, and is aligned normally in the Y direction.
   
   :param font: The loaded font to render the glyph with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param ch: The UNICODE (UCS-2) integer of the glyph to render.
   :type ch: int
   :param fg: The color to render the glyph in. This becomes colormap index 1.
   :type fg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderText_Shaded(font, text, fg, bg)

   Renders a string of ASCII encoded text to a new 8-bit palettized surface
   with a solid background and antialiasing, using the given font and colors.
   
   The 0 pixel is background, while other pixels have varying degrees of the
   foreground color. This results in a box of the background color around the
   text in the foreground color. 

   This is the second-fastest of the text rendering types, being slightly
   faster than :func:`TTF_RenderText_Blended` but slower than
   :func:`TTF_RenderText_Solid`. The rendered text will be antialiased, but the resulting
   surface will have a solid background colour instead of a transparent one.
   Surfaces rendered with this function should blit as quickly as those created
   with :func:`TTF_RenderText_Blended`. This rendering type should
   be used in cases when you want nice-looking text but don't need background
   transparency.
   
   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: The ASCII string to render.
   :type text: bytes
   :param fg: The color to render the text in. This becomes colormap index 1.
   :type fg: :obj:`SDL_Color`
   :param bg: The color to fill the background with. This becomes colormap
     index 0.
   :type bg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderUTF8_Shaded(font, text, fg, bg)

   Renders a string of UTF-8 encoded text to a new 8-bit palettized surface
   with a solid background and antialiasing, using the given font and color. 
   See :func:`TTF_RenderText_Shaded` for more info.
   
   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: The UTF-8 string to render.
   :type text: bytes
   :param fg: The color to render the text in. This becomes colormap index 1.
   :type fg: :obj:`SDL_Color`
   :param bg: The color to fill the background with. This becomes colormap
     index 0.
   :type bg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderUNICODE_Shaded(font, text, fg, bg)
   
   Renders a string of UCS-2 encoded text to a new 8-bit palettized surface
   with a solid background and antialiasing, using the given font and color. 
   See :func:`TTF_RenderText_Shaded` for more info.

   The expected input format for this function, along with its pitfalls, is
   described in the documentation for :func:`TTF_RenderUNICODE_Solid`.
   
   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: A ctypes uint16 array containing the glyphs of the UCS-2 string
     to render.
   :type text: POINTER(Uint16)
   :param fg: The color to render the text in. This becomes colormap index 1.
   :type fg: :obj:`SDL_Color`
   :param bg: The color to fill the background with. This becomes colormap
     index 0.
   :type bg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderGlyph_Shaded(font, ch, fg, bg)
   
   Renders a single UNICODE (UCS-2) glyph to a new 8-bit palettized surface
   with a solid background and antialiasing, using the given font and colors.

   The 0 pixel is the colorkey, giving a transparent background, and the 1
   pixel is set to the text color. The glyph is rendered without any padding
   or centering in the X direction, and is aligned normally in the Y direction.
   
   :param font: The loaded font to render the glyph with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param ch: The UNICODE (UCS-2) integer of the glyph to render.
   :type ch: int
   :param fg: The color to render the glyph in. This becomes colormap index 1.
   :type fg: :obj:`SDL_Color`
   :param bg: The color to fill the background with. This becomes colormap
     index 0.
   :type bg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderText_Blended(font, text, fg)

   Renders a string of ASCII encoded text to a new 32-bit ARGB surface with
   a transparent background and antialiasing, using the given font and color.

   This is the slowest (but best looking) of the text rendering types. The
   rendered text will be antialiased on a transparent surface using alpha
   blending. Surfaces rendered with this function will blit slower than those
   rendered with :func:`TTF_RenderText_Solid` or :func:`TTF_RenderText_Shaded`.
   This rendering type should be used in cases when you want to overlay
   rendered text over something else, and in in most other cases where high
   performance isn't a major concern.

   .. note:: To render an RGBA surface instead of an ARGB one, just swap the
             R and B values when creating the SDL_Color.
   
   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: The ASCII string to render.
   :type text: bytes
   :param fg: The color to render the text in.
   :type fg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderUTF8_Blended(font, text, fg)
   
   Renders a string of UTF-8 encoded text to a new 32-bit ARGB surface with
   a transparent background and antialiasing, using the given font and color.
   See :func:`TTF_RenderText_Blended` for more info.

   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: The UTF-8 string to render.
   :type text: bytes
   :param fg: The color to render the text in.
   :type fg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderUNICODE_Blended(font, text, fg)
   
   Renders a string of UCS-2 encoded text to a new 32-bit ARGB surface with
   a transparent background and antialiasing, using the given font and color.
   See :func:`TTF_RenderText_Blended` for more info.

   The expected input format for this function, along with its pitfalls, is
   described in the documentation for :func:`TTF_RenderUNICODE_Solid`.

   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: A ctypes uint16 array containing the glyphs of the UCS-2 string
     to render.
   :type text: POINTER(Uint16)
   :param fg: The color to render the text in.
   :type fg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderGlyph_Blended(font, ch, fg)

   Renders a single UNICODE (UCS-2) glyph to a new 32-bit ARGB surface with a
   transparent background and antialiasing, using the given font and color.

   The rendered glyph will be antialiased on a transparent surface using alpha
   blending. The glyph is rendered without any padding or centering in the X
   direction, and is aligned normally in the Y direction.
   
   :param font: The loaded font to render the glyph with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param ch: The UNICODE (UCS-2) integer of the glyph to render.
   :type ch: int
   :param fg: The color to render the glyph in.
   :type fg: :obj:`SDL_Color`
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderText_Blended_Wrapped(font, text, fg, wrapLength)

   Renders a string of ASCII encoded text to a new 32-bit ARGB surface with
   a transparent background and antialiasing, using the given font and color.
   Text is wrapped to multiple lines on line endings and on word boundaries
   if it extends beyond wrapLength in pixels.

   See :func:`TTF_RenderText_Blended` for more info.
   
   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: The ASCII string to render.
   :type text: bytes
   :param fg: The color to render the text in.
   :type fg: :obj:`SDL_Color`
   :param wrapLength: The maximum width of the text in pixels.
   :type wrapLength: int
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderUTF8_Blended_Wrapped(font, text, fg, wrapLength)
   
   Renders a string of UTF-8 encoded text to a new 32-bit ARGB surface with
   a transparent background and antialiasing, using the given font and color.
   Text is wrapped to multiple lines on line endings and on word boundaries
   if it extends beyond wrapLength in pixels.

   See :func:`TTF_RenderText_Blended` for more info.
   
   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: The UTF-8 string to render.
   :type text: bytes
   :param fg: The color to render the text in.
   :type fg: :obj:`SDL_Color`
   :param wrapLength: The maximum width of the text in pixels.
   :type wrapLength: int
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: TTF_RenderUNICODE_Blended_Wrapped(font, text, fg, wrapLength)
   
   Renders a string of UCS-2 encoded text to a new 32-bit ARGB surface with
   a transparent background and antialiasing, using the given font and color.
   Text is wrapped to multiple lines on line endings and on word boundaries
   if it extends beyond wrapLength in pixels.

   See :func:`TTF_RenderText_Blended` and :func:`TTF_RenderUNICODE_Solid` for
   more info.
   
   :param font: The loaded font to render the text with.
   :type font: POINTER(:obj:`TTF_Font`)
   :param text: A ctypes uint16 array containing the glyphs of the UCS-2 string
     to render.
   :type text: POINTER(Uint16)
   :param fg: The color to render the text in.
   :type fg: :obj:`SDL_Color`
   :param wrapLength: The maximum width of the text in pixels.
   :type wrapLength: int
   
   :returns: A pointer to the new surface containing the rendered text, or
     ``None`` if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)
   


Module constants
----------------

.. data:: TTF_MAJOR_VERSION

    Latest SDL2_ttf library major number supported by PySDL2.

.. data:: TTF_MINOR_VERSION

    Latest SDL2_ttf library minor number supported by PySDL2. 

.. data:: TTF_PATCHLEVEL

    Latest SDL2_ttf library patch level number supported by PySDL2.

.. data:: UNICODE_BOM_NATIVE

    This allows you to switch byte-order of UNICODE (UCS-2) text data to
    native order, meaning the mode of your CPU. This is meant to be used
    in UNICODE strings that you are using with the SDL2_ttf API. Not needed
    for UTF8 strings.

.. data:: UNICODE_BOM_SWAPPED

    This allows you to switch byte-order of UNICODE (UCS-2) text data to
    swapped order, meaning the reversed mode of your CPU. Thus, if your CPU
    is LSB, then the data will be interpretted as MSB. This is meant to be
    used in UNICODE strings that you are using with the SDL2_ttf API. Not
    needed for UTF8 strings.

.. data:: TTF_STYLE_NORMAL

    Used to indicate regular, normal, plain rendering style. 

.. data:: TTF_STYLE_BOLD

    Used to indicate bold rendering style. This is used in a bitmask along
    with other styles.

.. data:: TTF_STYLE_ITALIC

    Used to indicate italicized rendering style. This is used in a bitmask
    along with other styles.

.. data:: TTF_STYLE_UNDERLINE

    Used to indicate underlined rendering style. This is used in a bitmask
    along with other styles.

.. data:: TTF_STYLE_STRIKETHROUGH

    Used to indicate strikethrough rendering style. This is used in a bitmask
    along with other styles.

.. data:: TTF_HINTING_NORMAL

    Used to indicate set hinting type to normal.
    This corresponds to the default hinting algorithm, optimized for standard
    gray-level rendering.                              

.. data:: TTF_HINTING_LIGHT

    Used to indicate set hinting type to light.
    A lighter hinting algorithm for non-monochrome modes. Many generated
    glyphs are more fuzzy but better resemble its original shape. A bit like
    rendering on macOS.

.. data:: TTF_HINTING_MONO

    Used to indicate set hinting type to monochrome.
    Strong hinting algorithm that should only be used for monochrome output.
    The result is probably unpleasant if the glyph is rendered in
    non-monochrome modes.

.. data:: TTF_HINTING_NONE

    Used to indicate set hinting type to none.
    No hinting is used, so the font may become very blurry or messy at
    smaller sizes.
