import sys
import pytest
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_VIDEO
from sdl2 import blendmode


class TestSDLBlendmode(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        if SDL_Init(SDL_INIT_VIDEO) != 0:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    @pytest.mark.skip("not implemented")
    def test_SDL_ComposeCustomBlendMode(self):
        pass
