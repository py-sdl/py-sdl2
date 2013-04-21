import sys
import unittest
from .. import ext as sdl2ext
from ..ext.compat import byteify
from .. import surface

RESOURCES = sdl2ext.Resources(__file__, "resources")
FONTMAP = ["0123456789",
           "ABCDEFGHIJ",
           "KLMNOPQRST",
           "UVWXYZ    ",
           "abcdefghij",
           "klmnopqrst",
           "uvwxyz    ",
           ",;.:!?-+()"
           ]


class VideoFontTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        sdl2ext.init()

    def tearDown(self):
        sdl2ext.quit()

    def test_BitmapFont(self):
        sf = surface.SDL_LoadBMP(byteify(RESOURCES.get_path("font.bmp"), "utf-8"))
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        font = sdl2ext.BitmapFont(sf, (32, 32), FONTMAP)
        self.assertIsInstance(font, sdl2ext.BitmapFont)

        sprite = sdl2ext.SoftwareSprite(sf.contents, True)
        self.assertIsInstance(sprite, sdl2ext.SoftwareSprite)
        font = sdl2ext.BitmapFont(sprite, (32, 32), FONTMAP)
        self.assertIsInstance(font, sdl2ext.BitmapFont)

    @unittest.skip("not implemented")
    def test_BitmapFont_render(self):
        pass

    @unittest.skip("not implemented")
    def test_BitmapFont_render_on(self):
        pass

    @unittest.skip("not implemented")
    def test_BitmapFont_contains(self):
        pass

    @unittest.skip("not implemented")
    def test_BitmapFont_can_render(self):
        pass

if __name__ == '__main__':
    sys.exit(unittest.main())
