# coding=utf-8
import sys
import unittest
from .. import ext as sdl2ext
from ..ext.compat import byteify
from .. import surface, sdlttf

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


class SDL2ExtFontTest(unittest.TestCase):
    __tags__ = ["sdl", "sdl2ext"]

    def setUp(self):
        sdl2ext.init()

    def tearDown(self):
        sdl2ext.quit()

    def test_BitmapFont(self):
        sf = surface.SDL_LoadBMP(byteify(RESOURCES.get_path("font.bmp"),
                                         "utf-8"))
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

    def test_BitmapFont_contains(self):
        sf = surface.SDL_LoadBMP(byteify(RESOURCES.get_path("font.bmp"),
                                         "utf-8"))
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        font = sdl2ext.BitmapFont(sf, (32, 32), FONTMAP)
        self.assertIsInstance(font, sdl2ext.BitmapFont)

        for ch in "abcde12345.-,+":
            self.assertTrue(font.contains(ch))
        for ch in "äöüß":
            self.assertFalse(font.contains(ch))

    def test_BitmapFont_can_render(self):
        sf = surface.SDL_LoadBMP(byteify(RESOURCES.get_path("font.bmp"),
                                         "utf-8"))
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        font = sdl2ext.BitmapFont(sf, (32, 32), FONTMAP)
        self.assertIsInstance(font, sdl2ext.BitmapFont)

        self.assertTrue(font.can_render("text"))
        self.assertTrue(font.can_render("473285435hfsjadfhriuewtrhefd"))
        self.assertFalse(font.can_render("testä"))

    def test_FontManager(self):
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"),
                                 bg_color=(100, 0, 0))
        self.assertIsInstance(fm, sdl2ext.FontManager)
        self.assertEqual(fm.default_font, "tuffy")
        self.assertEqual(fm.size, 16)
        self.assertEqual(fm.bg_color, sdl2ext.Color(100, 0, 0, 0))

    def test_FontManager_default_font(self):
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"))
        self.assertEqual(fm.default_font, "tuffy")
        self.assertEqual(fm.size, 16)
        with self.assertRaises(ValueError):
            fm.default_font = "Inexistent Alias"
        fm.add(RESOURCES.get_path("tuffy.copy.ttf"), size = 10)
        fm.default_font = "tuffy.copy"
        fm.size = 10
        self.assertEqual(fm.default_font, "tuffy.copy")
        self.assertEqual(fm.size, 10)
        fm.default_font = "tuffy.copy"
        fm.size = 16
        self.assertEqual(fm.default_font, "tuffy.copy")
        self.assertEqual(fm.size, 16)

    def test_FontManager_add(self):
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"))
        self.assertIn("tuffy", fm.aliases)
        self.assertIn("tuffy", fm.fonts)
        self.assertIn(16, fm.fonts["tuffy"])
        self.assertIsInstance(fm.fonts["tuffy"][16].contents, sdlttf.TTF_Font)

        # Do some metrics tests
        font = fm.fonts["tuffy"][16]
        self.assertEqual(16, sdlttf.TTF_FontAscent(font))
        fm.add(RESOURCES.get_path("tuffy.ttf"), size=12)
        font = fm.fonts["tuffy"][12]
        self.assertEqual(12, sdlttf.TTF_FontAscent(font))

        self.assertRaises(IOError, fm.add, "inexistent.ttf")
        # I don't find a scenario raising a TTF_Error.
        # self.assertRaises(sdl2ext.SDLError, fm.add, "resources/tuffy.ttf",
        #                   size=-1)

        # Close the font manager and add a new font
        fm.close()
        fm.add(RESOURCES.get_path("tuffy.ttf"), size=12)
        self.assertIsInstance(fm.fonts["tuffy"][12].contents, sdlttf.TTF_Font)

    def test_FontManager_close(self):
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"))
        fm.add(RESOURCES.get_path("tuffy.ttf"), size=20)
        fm.add(RESOURCES.get_path("tuffy.ttf"), alias="Foo", size=10)
        fm.close()
        self.assertEqual(fm.fonts, {})
        # How to make sure TTF_CloseFont was called on each loaded font?

    def test_FontManager_render(self):
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"))
        text_surf = fm.render("text")
        self.assertIsInstance(text_surf, surface.SDL_Surface)
        self.assertTrue(text_surf.w > 1)

        text_surf = fm.render("text", size=10)
        self.assertIsInstance(text_surf, surface.SDL_Surface)

        text_surf = fm.render("""
text long enough to have it wrapped at 100 px width.""", size=20, width=100)
        self.assertIsInstance(text_surf, surface.SDL_Surface)
        self.assertTrue(text_surf.w > 1)
        self.assertTrue(text_surf.w == 100)
        self.assertRaises(KeyError, fm.render, "text", alias="inexistent")


if __name__ == '__main__':
    sys.exit(unittest.main())
