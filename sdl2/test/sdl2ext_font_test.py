# -*- coding: utf-8 -*-
import pytest
from sdl2 import ext as sdl2ext
from sdl2.ext.compat import byteify, ExperimentalWarning
from sdl2.ext.pixelaccess import pixels2d
from sdl2 import surface, sdlttf


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


class TestSDL2ExtFont(object):
    __tags__ = ["sdl", "sdl2ext"]

    @classmethod
    def setup_class(cls):
        try:
            sdl2ext.init()
        except sdl2ext.SDLError:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        sdl2ext.quit()

    def test_BitmapFont(self):
        # Initialize surface and sprite for tests
        fontpath = byteify(RESOURCES.get_path("font.bmp"), "utf-8")
        sf = surface.SDL_LoadBMP(fontpath)
        sprite = sdl2ext.SoftwareSprite(sf.contents, True)

        # Try SoftwareSprite surface
        font = sdl2ext.BitmapFont(sprite, (32, 32), FONTMAP)
        assert font.size == (32, 32)

        # Try SDL_Surface surface
        font = sdl2ext.BitmapFont(sf.contents, (32, 32), FONTMAP)
        assert font.size == (32, 32)

        # Try SDL_Surface pointer surface
        font = sdl2ext.BitmapFont(sf, (32, 32), FONTMAP)
        assert font.size == (32, 32)

        # Try invalid surface type
        with pytest.raises(TypeError):
            font = sdl2ext.BitmapFont("hello", (32, 32), FONTMAP)

    def test_BitmapFont_render(self):
        # Initialize font and BitmapFont for tests
        fontpath = byteify(RESOURCES.get_path("font.bmp"), "utf-8")
        sf = surface.SDL_LoadBMP(fontpath)
        font = sdl2ext.BitmapFont(sf.contents, (32, 32), FONTMAP)

        # Try rendering some text
        msg = "hello there!"
        text = font.render(msg)
        assert isinstance(text, sdl2ext.SoftwareSprite)
        assert text.size[0] == 32 * len(msg)

        # Test exception for missing glyph
        with pytest.raises(ValueError):
            font.render("this_should_fail")

    def test_BitmapFont_render_on(self):
        np = pytest.importorskip("numpy", reason="numpy module is not available")
        # Initialize font, surface, and BitmapFont for tests
        fontpath = byteify(RESOURCES.get_path("font.bmp"), "utf-8")
        sf = surface.SDL_LoadBMP(fontpath)
        font = sdl2ext.BitmapFont(sf.contents, (32, 32), FONTMAP)

        # Try rendering some text
        target = surface.SDL_CreateRGBSurface(0, 32*5, 32, 32, 0, 0, 0, 0)
        with pytest.warns(ExperimentalWarning):
            view = pixels2d(target, transpose=False)
        mid_row = view[16, :].copy()
        font.render_on(target, "TEST!")
        assert not np.all(mid_row == view[16, :]) # ensure surface changed

        # Try rendering some text with an offset
        target2 = surface.SDL_CreateRGBSurface(0, 32*5, 32, 32, 0, 0, 0, 0)
        with pytest.warns(ExperimentalWarning):
            view2 = pixels2d(target2, transpose=False)
        font.render_on(target2, "TEST!", offset=(5, 0))
        assert not np.all(mid_row == view2[16, :]) # ensure surface changed
        assert not np.all(view[16, :] == view2[16, :]) # ensure offset worked

        # Test exception for missing glyph
        with pytest.raises(ValueError):
            font.render_on(target, "%nope")

    def test_BitmapFont_contains(self):
        sf = surface.SDL_LoadBMP(byteify(RESOURCES.get_path("font.bmp"),
                                         "utf-8"))
        assert isinstance(sf.contents, surface.SDL_Surface)
        font = sdl2ext.BitmapFont(sf, (32, 32), FONTMAP)
        assert isinstance(font, sdl2ext.BitmapFont)

        for ch in "abcde12345.-,+":
            assert font.contains(ch)
        for ch in "äöüß":
            assert not font.contains(ch)

    def test_BitmapFont_can_render(self):
        sf = surface.SDL_LoadBMP(byteify(RESOURCES.get_path("font.bmp"),
                                         "utf-8"))
        assert isinstance(sf.contents, surface.SDL_Surface)
        font = sdl2ext.BitmapFont(sf, (32, 32), FONTMAP)
        assert isinstance(font, sdl2ext.BitmapFont)

        assert font.can_render("text")
        assert font.can_render("473285435hfsjadfhriuewtrhefd")
        assert not font.can_render("testä")

    def test_FontManager(self):
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"),
                                 bg_color=(100, 0, 0))
        assert isinstance(fm, sdl2ext.FontManager)
        assert fm.default_font == "tuffy"
        assert fm.size == 16
        assert fm.bg_color == sdl2ext.Color(100, 0, 0, 0)

    def test_FontManager_default_font(self):
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"))
        assert fm.default_font == "tuffy"
        assert fm.size == 16
        with pytest.raises(ValueError):
            fm.default_font = "Inexistent Alias"
        fm.add(RESOURCES.get_path("tuffy.copy.ttf"), size = 10)
        fm.default_font = "tuffy.copy"
        fm.size = 10
        assert fm.default_font == "tuffy.copy"
        assert fm.size == 10
        fm.default_font = "tuffy.copy"
        fm.size = 16
        assert fm.default_font == "tuffy.copy"
        assert fm.size == 16

    def test_FontManager_add(self):
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"))
        assert "tuffy" in fm.aliases
        assert "tuffy" in fm.fonts
        assert 16 in fm.fonts["tuffy"]
        assert isinstance(fm.fonts["tuffy"][16].contents, sdlttf.TTF_Font)

        # Do some metrics tests
        # NOTE: Ascent & other font metrics changed in FreeType 2.10, so we 
        # test against both < 2.10 and >= 2.10 values
        font = fm.fonts["tuffy"][16]
        assert sdlttf.TTF_FontAscent(font) in [13, 16]
        fm.add(RESOURCES.get_path("tuffy.ttf"), size=12)
        font = fm.fonts["tuffy"][12]
        assert sdlttf.TTF_FontAscent(font) in [10, 12]

        with pytest.raises(IOError):
            fm.add("inexistent.ttf")
        # I don't find a scenario raising a TTF_Error.
        # self.assertRaises(sdl2ext.SDLError, fm.add, "resources/tuffy.ttf",
        #                   size=-1)

        # Close the font manager and add a new font
        fm.close()
        fm.add(RESOURCES.get_path("tuffy.ttf"), size=12)
        assert isinstance(fm.fonts["tuffy"][12].contents, sdlttf.TTF_Font)

    def test_FontManager_close(self):
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"))
        fm.add(RESOURCES.get_path("tuffy.ttf"), size=20)
        fm.add(RESOURCES.get_path("tuffy.ttf"), alias="Foo", size=10)
        fm.close()
        assert fm.fonts == {}
        # How to make sure TTF_CloseFont was called on each loaded font?

    def test_FontManager_render(self):
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"))
        text_surf = fm.render("text")
        assert isinstance(text_surf, surface.SDL_Surface)
        assert text_surf.w > 1

        text_surf = fm.render("text", size=10)
        assert isinstance(text_surf, surface.SDL_Surface)

        text_surf = fm.render("""
text long enough to have it wrapped at 100 px width.""", size=20, width=100)
        assert isinstance(text_surf, surface.SDL_Surface)
        assert text_surf.w > 1
        assert text_surf.w == 100
        with pytest.raises(KeyError):
            fm.render("text", alias="inexistent")
