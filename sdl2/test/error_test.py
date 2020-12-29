import sys
import pytest
import sdl2
from sdl2 import SDL_Init, SDL_Quit, error


class TestSDLError(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        SDL_Init(0)

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    def test_SDL_GetSetClearError(self):
        assert error.SDL_GetError() == b""
        error.SDL_SetError(b"A Unit Test Error Message")
        assert error.SDL_GetError() == b"A Unit Test Error Message"
        error.SDL_ClearError()
        assert error.SDL_GetError() == b""
        error.SDL_SetError(b"A Unit Test Error Message")
        assert error.SDL_GetError() == b"A Unit Test Error Message"
        assert error.SDL_GetError() == b"A Unit Test Error Message"
        error.SDL_ClearError()
        error.SDL_SetError(b"123456789")
        assert error.SDL_GetError() == b"123456789"

    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GetErrorMsg(self):
        error.SDL_SetError(b"123456789")
        assert error.SDL_GetError() == b"123456789"
        assert error.SDL_GetErrorMsg(b' ' * 10, 10) == b"123456789"
        assert error.SDL_GetErrorMsg(b' ' * 5, 5) == b"1234"
        error.SDL_ClearError()
