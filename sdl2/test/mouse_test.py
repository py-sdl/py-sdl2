import sys
import pytest
from sdl2 import mouse


@pytest.mark.skip("not implemented")
class TestSDLMouse(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
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