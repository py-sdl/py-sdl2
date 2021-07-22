import sys
import pytest
from sdl2.surface import SDL_CreateRGBSurface
from sdl2.rect import SDL_Rect
from sdl2.ext.color import Color, COLOR
from sdl2.ext.compat import ExperimentalWarning
from sdl2 import ext as sdl2ext


class TestSDL2ExtDraw(object):
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

    @pytest.mark.skipif(hasattr(sys, "pypy_version_info"),
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_fill(self):
        # Initialize colour and surface/view
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        with pytest.warns(ExperimentalWarning):
            view = sdl2ext.pixels3d(sf.contents, False)

        # Test with no provided fill area
        sdl2ext.fill(sf.contents, WHITE, None)
        assert all(x == 255 for x in view[0][0][:3])
        assert all(x == 255 for x in view[-1][-1][:3])

        # Test with SDL_Rect fill area
        sdl2ext.fill(sf.contents, BLACK, None)  # reset surface
        r = SDL_Rect(0, 0, 5, 5)
        sdl2ext.fill(sf.contents, WHITE, r)
        assert all(x == 255 for x in view[0][0][:3])
        assert all(x == 255 for x in view[4][4][:3])
        assert all(x == 0 for x in view[-1][-1][:3])

        # Test with tuple fill area
        sdl2ext.fill(sf.contents, BLACK, None)  # reset surface
        r = (5, 5, 5, 5)
        sdl2ext.fill(sf.contents, WHITE, r)
        assert all(x == 0 for x in view[4][4][:3])
        assert all(x == 255 for x in view[5][5][:3])
        assert all(x == 255 for x in view[-1][-1][:3])

        # Test with multiple fill areas
        sdl2ext.fill(sf.contents, BLACK, None)  # reset surface
        rects = [(0, 0, 10, 5), SDL_Rect(0, 0, 3, 10), (7, 7, 3, 10)]
        sdl2ext.fill(sf.contents, WHITE, rects)
        assert all(x == 255 for x in view[0][0][:3])
        assert all(x == 255 for x in view[0][-1][:3])
        assert all(x == 255 for x in view[-1][-1][:3])
        assert all(x == 0 for x in view[-1][4][:3])

        # Test exception on bad input
        with pytest.raises(ValueError):
            sdl2ext.fill(sf.contents, WHITE, (1, 2, 3))

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
            assert c == int(color)
        for color in icolors:
            c = sdl2ext.prepare_color(color, sprite)
            cc = COLOR(color)
            assert c == int(cc)
        for color in scolors:
            c = sdl2ext.prepare_color(color, sprite)
            cc = COLOR(color)
            assert c == int(cc)
