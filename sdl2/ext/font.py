"""Font and text rendering routines."""
import os
from .. import surface, rect
from .sprite import SoftwareSprite


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
        #elif isinstance(surface, sprite.Sprite):
        #    TODO
        elif isinstance(imgsurface, surface.SDL_Surface):
            self.surface = imgsurface
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

    def render(self, text, bpp=None):
        """Renders the passed text on a new Sprite and returns it."""
        x, y = 0, 0
        tw, th = 0, 0
        w, h = self.size
        # TODO
        lines = text.split(os.linesep)
        for line in lines:
            tw = max(tw, sum([w for c in line]))
            th += h

        if bpp is None:
            bpp = self.surface.format.BitsPerPixel
        imgsurface = SoftwareSprite(tw, th, bpp)
        target = imgsurface.surface
        blit_surface = surface.SDL_BlitSurface
        fontsf = self.surface
        offsets = self.offsets

        srcr = rect.SDL_Rect(0, 0, 0, 0)
        for line in lines:
            for c in line:
                srcr.x = x
                srcr.y = y
                blit_surface(target, srcr, fontsf, offsets[c])
                x += w
            y += h
        return imgsurface

    def render_on(self, imgsurface, text, offset=(0, 0)):
        """Renders a text on the passed sprite, starting at a specific
        offset.

        The top-left start position of the text will be the passed offset and
        4-value tuple with the changed area will be returned.
        """
        x, y = offset
        w, h = self.size

        target = None
        if isinstance(imgsurface, SoftwareSprite):
            target = imgsurface.surface
        #elif isinstance(surface, sprite.Sprite):
        #    TODO
        elif isinstance(imgsurface, surface.SDL_Surface):
            target = imgsurface
        else:
            raise TypeError("unsupported surface type")

        lines = text.split(os.linesep)
        blit_surface = surface.SDL_BlitSurface
        fontsf = self.surface
        offsets = self.offsets

        srcr = rect.SDL_Rect(0, 0, 0, 0)
        for line in lines:
            for c in line:
                srcr.x = x
                srcr.y = y
                blit_surface(target, srcr, fontsf, offsets[c])
                x += w
            y += h
        return (offset[0], offset[1], x + w, y + h)

    def contains(self, c):
        """Checks, whether a certain character exists in the font."""
        return c in self.offsets

    def can_render(self, text):
        """Checks, whether all characters in the passed text can be rendered.
        """
        lines = text.split(os.linesep)
        for line in lines:
            for c in line:
                if c not in self.offsets:
                    return False
        return True
