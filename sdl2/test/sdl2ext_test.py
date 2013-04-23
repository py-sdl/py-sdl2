import sys
import unittest
from .. import ext as sdl2ext
from .. import SDL_WasInit, SDL_INIT_VIDEO


class SDL2ExtTest(unittest.TestCase):
    __tags__ = ["sdl", "sdl2ext"]

    def test_init_quit(self):
        sdl2ext.init()
        self.assertEqual(SDL_WasInit(SDL_INIT_VIDEO), SDL_INIT_VIDEO)
        sdl2ext.quit()
        self.assertNotEqual(SDL_WasInit(SDL_INIT_VIDEO), SDL_INIT_VIDEO)
        sdl2ext.init()
        sdl2ext.init()
        sdl2ext.init()
        self.assertEqual(SDL_WasInit(SDL_INIT_VIDEO), SDL_INIT_VIDEO)
        sdl2ext.quit()
        self.assertNotEqual(SDL_WasInit(SDL_INIT_VIDEO), SDL_INIT_VIDEO)
        sdl2ext.quit()
        sdl2ext.quit()
        sdl2ext.quit()
        self.assertNotEqual(SDL_WasInit(SDL_INIT_VIDEO), SDL_INIT_VIDEO)

    @unittest.skip("not implemented")
    def test_get_events(self):
        pass

    def test_TestEventProcessor(self):
        proc = sdl2ext.TestEventProcessor()
        self.assertIsInstance(proc, sdl2ext.TestEventProcessor)


if __name__ == '__main__':
    sys.exit(unittest.main())
