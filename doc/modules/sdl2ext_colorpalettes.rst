.. module:: sdl2.ext.colorpalettes
   :synopsis: Predefined sets of colors.

sdl2.ext.colorpalettes - predefined sets of colors
==================================================
Indexed color palettes. Each palette is a tuple of
:class:`sdl2.ext.Color` objects.

The following palettes are currently available:

================== ===================================================
Palette Identifier Description
================== ===================================================
MONOPALETTE        1-bit monochrome palette (black and white).

GRAY2PALETTE       2-bit grayscale palette with black, white and two
                   shades of gray.
GRAY4PALETTE       4-bit grayscale palette with black, white and 14
                   shades shades of gray.
GRAY8PALETTE       8-bit grayscale palette with black, white and 254
                   shades shades of gray.
RGB3PALETTE        3-bit RGB color palette with pure red, green and
                   blue and their complementary colors as well as black
                   and white.
CGAPALETTE         CGA color palette.
EGAPALETTE         EGA color palette.
VGAPALETTE         8-bit VGA color palette.
WEBPALETTE         "Safe" web color palette with 225 colors.
================== ===================================================
