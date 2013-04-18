import sys
import unittest
from .. import SDL_Init, SDL_WasInit, SDL_InitSubSystem, SDL_QuitSubSystem, \
    SDL_Quit, SDL_INIT_AUDIO, SDL_INIT_EVERYTHING, SDL_INIT_GAMECONTROLLER, \
    SDL_INIT_HAPTIC, SDL_INIT_JOYSTICK, SDL_INIT_NOPARACHUTE, SDL_INIT_TIMER, \
    SDL_INIT_VIDEO


class SDLTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(0)

    def tearDown(self):
        SDL_Quit()

    def test_SDL_INIT_TIMER(self):
        SDL_Init(SDL_INIT_TIMER)
        ret = SDL_WasInit(SDL_INIT_TIMER)
        self.assertEqual(ret, SDL_INIT_TIMER)
        SDL_QuitSubSystem(SDL_INIT_TIMER)

    def test_SDL_INIT_AUDIO(self):
        SDL_Init(SDL_INIT_AUDIO)
        ret = SDL_WasInit(SDL_INIT_AUDIO)
        self.assertEqual(ret, SDL_INIT_AUDIO)
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    def test_SDL_INIT_VIDEO(self):
        SDL_Init(SDL_INIT_VIDEO)
        ret = SDL_WasInit(SDL_INIT_VIDEO)
        self.assertEqual(ret, SDL_INIT_VIDEO)
        SDL_QuitSubSystem(SDL_INIT_VIDEO)

    def test_SDL_INIT_JOYSTICK(self):
        SDL_Init(SDL_INIT_JOYSTICK)
        ret = SDL_WasInit(SDL_INIT_JOYSTICK)
        self.assertEqual(ret, SDL_INIT_JOYSTICK)
        SDL_QuitSubSystem(SDL_INIT_JOYSTICK)

    def test_SDL_INIT_HAPTIC(self):
        SDL_Init(SDL_INIT_HAPTIC)
        ret = SDL_WasInit(SDL_INIT_HAPTIC)
        if sys.platform.startswith("freebsd"):
            # not supported yet
            self.assertNotEqual(ret, SDL_INIT_HAPTIC)
        else:
            self.assertEqual(ret, SDL_INIT_HAPTIC)
        SDL_QuitSubSystem(SDL_INIT_HAPTIC)


if __name__ == '__main__':
    sys.exit(unittest.main())
