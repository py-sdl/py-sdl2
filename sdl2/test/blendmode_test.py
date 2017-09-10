import sys
import unittest
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_VIDEO
from sdl2 import blendmode


class SDLBlendmodeTest(unittest.TestCase):
    __tags__ = ["sdl"]

    @classmethod
    def setUpClass(cls):
        SDL_Init(SDL_INIT_VIDEO)

    @classmethod
    def tearDownClass(cls):
        SDL_Quit()

    @unittest.skip("not implemented")
    def test_SDL_ComposeCustomBlendMode(self):
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
