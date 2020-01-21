import sys
import pytest
from sdl2 import SDL_Init, SDL_Quit, error


class TestSDL(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        SDL_Init(0)

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    def test_SDL_ClearError(self):
        error.SDL_ClearError()
        assert error.SDL_GetError() == b""

    def test_SDL_SetError(self):
        assert error.SDL_GetError() == b""
        error.SDL_SetError(b"A Unit Test Error Message")
        assert error.SDL_GetError() == b"A Unit Test Error Message"
        error.SDL_ClearError()
        error.SDL_SetError(b"A Unit Test Error Message")
        assert error.SDL_GetError() == b"A Unit Test Error Message"
        assert error.SDL_GetError() == b"A Unit Test Error Message"
        error.SDL_ClearError()
        error.SDL_SetError(b"123456789")
        assert error.SDL_GetError() == b"123456789"
