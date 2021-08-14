import pytest
from sdl2.surface import SDL_CreateRGBSurface, SDL_FillRect
from sdl2.rect import SDL_Rect
from sdl2.ext.draw import prepare_color, fill
from sdl2 import ext as sdl2ext


class TestSDL2ExtSurface(object):
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

    def test_subsurface(self):
        # Initialize colour and surface/view
        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        WHITE = prepare_color((255, 255, 255), sf)

        # Test creation of subsurface from parent
        ssf = sdl2ext.subsurface(sf.contents, (0, 0, 5, 5))
        assert ssf.w == 5 and ssf.h == 5

        # Test shared pixels between surface
        fill(ssf, (255, 255, 255))
        view = sdl2ext.pixels3d(sf.contents, False)
        assert all(x == 255 for x in view[0][0][:3])
        assert all(x == 255 for x in view[4][4][:3])
        assert all(x == 0 for x in view[5][5][:3])

        # Test exceptions on bad input
        with pytest.raises(TypeError):
            sdl2ext.subsurface(WHITE, (0, 0, 5, 5))
        with pytest.raises(TypeError):
            sdl2ext.subsurface(sf, (0, 0, 5))
        with pytest.raises(ValueError):
            sdl2ext.subsurface(sf, (0, 0, 50, 50))
