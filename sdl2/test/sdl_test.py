import sys
import unittest
from .. import SDL_Init, SDL_WasInit, SDL_InitSubSystem, SDL_QuitSubSystem, \
    SDL_Quit, SDL_INIT_AUDIO, SDL_INIT_EVERYTHING, SDL_INIT_GAMECONTROLLER, \
    SDL_INIT_HAPTIC, SDL_INIT_JOYSTICK, SDL_INIT_NOPARACHUTE, SDL_INIT_TIMER, \
    SDL_INIT_VIDEO, SDL_GetError


class SDLTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(0)

    def tearDown(self):
        SDL_Quit()

    def test_SDL_INIT_TIMER(self):
        ret = SDL_Init(SDL_INIT_TIMER)
        self.assertEqual(ret, 0, SDL_GetError())
        ret = SDL_WasInit(SDL_INIT_TIMER)
        self.assertEqual(ret, SDL_INIT_TIMER)
        SDL_QuitSubSystem(SDL_INIT_TIMER)

    def test_SDL_INIT_AUDIO(self):
        ret = SDL_Init(SDL_INIT_AUDIO)
        self.assertEqual(ret, 0, SDL_GetError())
        ret = SDL_WasInit(SDL_INIT_AUDIO)
        self.assertEqual(ret, SDL_INIT_AUDIO)
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    def test_SDL_INIT_VIDEO(self):
        ret = SDL_Init(SDL_INIT_VIDEO)
        self.assertEqual(ret, 0, SDL_GetError())
        ret = SDL_WasInit(SDL_INIT_VIDEO)
        self.assertEqual(ret, SDL_INIT_VIDEO)
        SDL_QuitSubSystem(SDL_INIT_VIDEO)

    def test_SDL_INIT_JOYSTICK(self):
        ret = SDL_Init(SDL_INIT_JOYSTICK)
        self.assertEqual(ret, 0, SDL_GetError())
        ret = SDL_WasInit(SDL_INIT_JOYSTICK)
        self.assertEqual(ret, SDL_INIT_JOYSTICK)
        SDL_QuitSubSystem(SDL_INIT_JOYSTICK)

    @unittest.skipIf(sys.platform.startswith("freebsd"),
                     "FreeBSD des not support haptic input yet")
    def test_SDL_INIT_HAPTIC(self):
        ret = SDL_Init(SDL_INIT_HAPTIC)
        self.assertEqual(ret, 0, SDL_GetError())
        ret = SDL_WasInit(SDL_INIT_HAPTIC)
        self.assertEqual(ret, SDL_INIT_HAPTIC)
        SDL_QuitSubSystem(SDL_INIT_HAPTIC)


if __name__ == '__main__':
    sys.exit(unittest.main())
