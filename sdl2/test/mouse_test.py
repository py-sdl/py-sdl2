import sys
import unittest
from .. import mouse


@unittest.skip("not implemented")
class SDLMouseTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_SDL_GetMouseFocus(self):
        pass

    def test_SDL_GetMouseState(self):
        pass

    def test_SDL_GetRelativeMouseState(self):
        pass

    def test_SDL_WarpMouseInWindow(self):
        pass

    def test_SDL_GetSetRelativeMouseMode(self):
        pass

    def test_SDL_CreateFreeCursor(self):
        pass

    def test_SDL_CreateColorCursor(self):
        pass

    def test_SDL_CreateSystemCursor(self):
        pass

    def test_SDL_GetSetCursor(self):
        pass

    def test_SDL_GetDefaultCursor(self):
        pass

    def test_SDL_ShowCursor(self):
        pass

    def test_SDL_WarpMouseGlobal(self):
        pass

    def test_SDL_CaptureMouse(self):
        pass

    def test_SDL_GetGlobalMouseState(self):
        pass

if __name__ == '__main__':
    sys.exit(unittest.main())
