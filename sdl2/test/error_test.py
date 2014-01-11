import sys
import unittest
from .. import SDL_Init, SDL_Quit, error


class SDLTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(0)

    def tearDown(self):
        SDL_Quit()

    def test_SDL_ClearError(self):
        error.SDL_ClearError()
        self.assertEqual(error.SDL_GetError(), b"")

    def test_SDL_SetError(self):
        self.assertEqual(error.SDL_GetError(), b"")
        error.SDL_SetError(b"A Unit Test Error Message")
        self.assertEqual(error.SDL_GetError(), b"A Unit Test Error Message")
        error.SDL_ClearError()
        error.SDL_SetError(b"A Unit Test Error Message")
        self.assertEqual(error.SDL_GetError(), b"A Unit Test Error Message")
        self.assertEqual(error.SDL_GetError(), b"A Unit Test Error Message")
        error.SDL_ClearError()
        error.SDL_SetError(b"123456789")
        self.assertEqual(error.SDL_GetError(), b"123456789")


if __name__ == '__main__':
    sys.exit(unittest.main())
