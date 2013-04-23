import sys
import unittest
from ..ext.color import Color, COLOR
from .. import ext as sdl2ext


class SDL2ExtDrawTest(unittest.TestCase):
    __tags__ = ["sdl", "sdl2ext"]

    def setUp(self):
        sdl2ext.init()

    def tearDown(self):
        sdl2ext.quit()

    @unittest.skipIf(hasattr(sys, "pypy_version_info"),
                     "PyPy's ctypes can't do byref(value, offset)")
    def test_fill(self):
        # TODO: add exceptions and more bounding tests.
        rects = ((0, 0, 3, 2),
                 (2, 3, 4, 2),
                 (5, -1, 2, 2),
                 (1, 7, 4, 8)
                 )
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        sprite = factory.create_sprite(size=(10, 10), bpp=32)
        view = sdl2ext.PixelView(sprite)
        for rect in rects:
            sdl2ext.fill(sprite, 0)
            colorval = sdl2ext.prepare_color(0xAABBCCDD, sprite)
            sdl2ext.fill(sprite, 0xAABBCCDD, rect)
            for y, row in enumerate(view):
                for x, col in enumerate(row):
                    if y >= rect[1] and y < (rect[1] + rect[3]):
                        if x >= rect[0] and x < (rect[0] + rect[2]):
                            self.assertEqual(col, colorval,
                                             "color mismatch at (x, y)")
                        else:
                            self.assertEqual(col, 0,
                                             "color mismatch at (x, y)")

                    else:
                        self.assertEqual(col, 0, "color mismatch at (x, y)")

    def test_prepare_color(self):
        rcolors = (Color(0, 0, 0, 0),
                   Color(255, 255, 255, 255),
                   Color(8, 55, 110, 220),
                   )
        icolors = (0x00000000,
                   0xFFFFFFFF,
                   0xAABBCCDD,
                   )
        scolors = ("#000",
                   "#FFF",
                   "#AABBCCDD",
                   )

        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        sprite = factory.create_sprite(size=(10, 10), bpp=32,
                                       masks=(0xFF000000,
                                              0x00FF0000,
                                              0x0000FF00,
                                              0x000000FF))

        for color in rcolors:
            c = sdl2ext.prepare_color(color, sprite)
            self.assertEqual(c, int(color))
        for color in icolors:
            c = sdl2ext.prepare_color(color, sprite)
            cc = COLOR(color)
            self.assertEqual(c, int(cc))
        for color in scolors:
            c = sdl2ext.prepare_color(color, sprite)
            cc = COLOR(color)
            self.assertEqual(c, int(cc))


if __name__ == '__main__':
    sys.exit(unittest.main())
