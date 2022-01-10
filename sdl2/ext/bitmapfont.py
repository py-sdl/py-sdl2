import os
from .. import surface, rect
from .common import SDLError
from .sprite import SoftwareSprite
from .draw import _get_target_surface


__all__ = ["BitmapFont"]


class BitmapFont(object):
    """A bitmap graphics to character mapping.

    The BitmapFont class uses an image surface to find and render font
    character glyphs for text. It requires a mapping table, which
    denotes the characters available on the image.

    The mapping table is a list of strings, where each string reflects a
    'line' of characters on the image. Each character within each line
    has the same size as specified by the size argument.

    A typical mapping table might look like

      [ '0123456789',
        'ABCDEFGHIJ',
        'KLMNOPQRST',
        'UVWXYZ    ',
        'abcdefghij',
        'klmnopqrst',
        'uvwxyz    ',
        ',;.:!?+-()' ]
    """

    DEFAULTMAP = ["0123456789",
                  "ABCDEFGHIJ",
                  "KLMNOPQRST",
                  "UVWXYZ    ",
                  "abcdefghij",
                  "klmnopqrst",
                  "uvwxyz    ",
                  ",;.:!?+-()"
                ]


    def __init__(self, imgsurface, size, mapping=None):
        """Creates a new BitmapFont instance from the passed image.

        Each character is expected to be of the same size (a 2-value tuple
        denoting the width and height) and to be in order of the passed
        mapping.
        """
        if mapping is None:
            self.mapping = list(BitmapFont.DEFAULTMAP)
        else:
            self.mapping = mapping
        self.offsets = {}
        if isinstance(imgsurface, SoftwareSprite):
            self.surface = imgsurface.surface
            self._sprite = imgsurface # prevent GC on the Sprite
        elif isinstance(imgsurface, surface.SDL_Surface):
            self.surface = imgsurface
        elif "SDL_Surface" in str(type(imgsurface)):
            self.surface = imgsurface.contents
        else:
            raise TypeError("imgsurface must be a Sprite or SDL_Surface")
        self.size = size[0], size[1]
        self._calculate_offsets()

    def _calculate_offsets(self):
        """Calculates the internal character offsets for each line."""
        self.offsets = {}
        offsets = self.offsets
        x, y = 0, 0
        w, h = self.size
        for line in self.mapping:
            x = 0
            for c in line:
                offsets[c] = rect.SDL_Rect(x, y, w, h)
                x += w
            y += h

    def _validate_chars(self, text):
        e = "The character '{0}' does not exist within the current font mapping"
        for ch in text:
            if ch not in self.offsets.keys():
                raise ValueError(e.format(ch))

    def _render_text(self, target, fontsf, lines, offset=(0, 0)):
        w, h = self.size
        dstr = rect.SDL_Rect(0, 0, 0, 0)
        y = offset[1]
        for line in lines:
            dstr.y = y
            x = offset[0]
            for c in line:
                dstr.x = x
                surface.SDL_BlitSurface(fontsf, self.offsets[c], target, dstr)
                x += w
            y += h
        return (x, y)

    def render(self, text, bpp=None):
        """Renders the passed text on a new Sprite and returns it."""
        w, h = self.size
        self._validate_chars(text)
        lines = text.split(os.linesep)

        tw, th = 0, 0
        for line in lines:
            tw = max(tw, sum([w for c in line]))
            th += h
        if bpp is None:
            bpp = self.surface.format.contents.BitsPerPixel
        sf = surface.SDL_CreateRGBSurface(0, tw, th, bpp, 0, 0, 0, 0)
        if not sf:
            raise SDLError()
        imgsurface = SoftwareSprite(sf.contents, False)

        self._render_text(imgsurface.surface, self.surface, lines)
        return imgsurface

    def render_on(self, imgsurface, text, offset=(0, 0)):
        """Renders a text on the passed sprite, starting at a specific
        offset.

        The top-left start position of the text will be the passed offset and
        4-value tuple with the changed area will be returned.
        """
        w, h = self.size
        target = _get_target_surface(imgsurface)
        self._validate_chars(text)
        lines = text.split(os.linesep)

        x, y = self._render_text(target, self.surface, lines, offset)
        return (offset[0], offset[1], x + w, y + h)

    def contains(self, c):
        """Checks, whether a certain character exists in the font."""
        return c == ' ' or c in self.offsets

    def can_render(self, text):
        """Checks, whether all characters in the passed text can be rendered.
        """
        lines = text.split(os.linesep)
        for line in lines:
            for c in line:
                if c != ' ' and c not in self.offsets:
                    return False
        return True
