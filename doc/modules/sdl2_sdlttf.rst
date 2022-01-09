.. currentmodule:: sdl2.sdlttf

sdl2.sdlttf - Python bindings for SDL_ttf
=========================================

py-sdl2 provides bindings for SDL2_ttf, a library designed for use with SDL2
that provides high quality TrueType font rendering.

SDL2_ttf supports a wide range of font formats, including TrueType (.ttf) and
OpenType (.otf) fonts. It also supports different font styles, font hinting
modes, and font outlines.

The SDL2_ttf library provides functions for rendering three main formats of
text, denoted by the suffix of the function. Functions ending in ``Text`` can only
render plain ASCII text, whereas functions ending in ``UTF8`` or ``UNICODE`` can
render most unicode characters provided that a font supports them. In general,
you should always use the ``UTF8`` rendering functions unless you have a strong
reason to do otherwise.

.. contents:: Table Of Contents
   :depth: 2
   :local:

.. note::
   This module handles font sizes in units of points (pt) instead of pixels. To
   obtain a font with a given pixel height, you can use the
   :func:`TTF_GlyphMetrics` function to get the pixel heights of different
   glyphs in the font at a given pt size and use the px/pt ratio to figure out
   the pt size needed to render text at a given height in px.

.. note::
   The surface sizes and contents of rendered text may vary slightly between
   systems depending on the version of FreeType used by SDL2_ttf.


Initialization functions
------------------------

.. autofunction:: TTF_Init

.. autofunction:: TTF_Quit

.. autofunction:: TTF_WasInit

.. autofunction:: TTF_ByteSwappedUNICODE

.. autofunction:: TTF_Linked_Version


Font loading functions
----------------------

.. autofunction:: TTF_OpenFont

.. autofunction:: TTF_OpenFontIndex

.. autofunction:: TTF_OpenFontRW

.. autofunction:: TTF_OpenFontIndexRW

.. autofunction:: TTF_CloseFont


Font attribute functions
------------------------

.. autofunction:: TTF_SetFontStyle

.. autofunction:: TTF_GetFontStyle

.. autofunction:: TTF_SetFontHinting

.. autofunction:: TTF_FontHeight

.. autofunction:: TTF_FontAscent

.. autofunction:: TTF_FontDescent

.. autofunction:: TTF_FontLineSkip

.. autofunction:: TTF_GetFontKerning

.. autofunction:: TTF_SetFontKerning

.. autofunction:: TTF_FontFaceIsFixedWidth

.. autofunction:: TTF_FontFaceFamilyName

.. autofunction:: TTF_FontFaceStyleName

.. autofunction:: TTF_GlyphIsProvided

.. autofunction:: TTF_GlyphMetrics

.. autofunction:: TTF_GetFontKerningSizeGlyphs


Text rendering functions
------------------------

Size calculation functions
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: TTF_SizeText

.. autofunction:: TTF_SizeUTF8

.. autofunction:: TTF_SizeUNICODE


Solid rendering functions
^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: TTF_RenderText_Solid

.. autofunction:: TTF_RenderUTF8_Solid

.. autofunction:: TTF_RenderUNICODE_Solid

.. autofunction:: TTF_RenderGlyph_Solid


Shaded rendering functions
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: TTF_RenderText_Shaded

.. autofunction:: TTF_RenderUTF8_Shaded

.. autofunction:: TTF_RenderUNICODE_Shaded

.. autofunction:: TTF_RenderGlyph_Shaded


Blended rendering functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: TTF_RenderText_Blended

.. autofunction:: TTF_RenderUTF8_Blended

.. autofunction:: TTF_RenderUNICODE_Blended

.. autofunction:: TTF_RenderGlyph_Blended

.. autofunction:: TTF_RenderText_Blended_Wrapped

.. autofunction:: TTF_RenderUTF8_Blended_Wrapped

.. autofunction:: TTF_RenderUNICODE_Blended_Wrapped


Data types
----------

.. autoclass:: TTF_Font


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
