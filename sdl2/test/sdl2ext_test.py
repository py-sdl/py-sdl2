import sys
import unittest
from .. import ext as sdl2ext
from .. import SDL_WasInit, SDL_INIT_VIDEO, SDL_FlushEvent, SDL_USEREVENT, \
    SDL_FIRSTEVENT, SDL_LASTEVENT, SDL_Event, SDL_UserEvent, SDL_PushEvent


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

    def test_get_events(self):
        sdl2ext.init()
        SDL_FlushEvent(SDL_FIRSTEVENT, SDL_LASTEVENT)
        for x in range(10):
            event = SDL_Event()
            event.type = SDL_USEREVENT + 1
            event.user = SDL_UserEvent(type=event.type, timestamp=0,
                                       windowID=0, code=0)
            SDL_PushEvent(event)
        results = sdl2ext.get_events()
        self.assertEqual(len(results), 10)
        for ev in results:
            self.assertEqual(ev.type, (SDL_USEREVENT + 1))

    def test_get_events_issue_6(self):
        sdl2ext.init()
        SDL_FlushEvent(SDL_FIRSTEVENT, SDL_LASTEVENT)
        for x in range(12):
            event = SDL_Event()
            event.type = SDL_USEREVENT + x
            event.user = SDL_UserEvent(type=event.type, timestamp=0,
                                       windowID=0, code=0)
            SDL_PushEvent(event)
        results = sdl2ext.get_events()
        for idx, r in enumerate(results):
            self.assertEqual(idx, r.type - SDL_USEREVENT)

    def test_TestEventProcessor(self):
        proc = sdl2ext.TestEventProcessor()
        self.assertIsInstance(proc, sdl2ext.TestEventProcessor)


if __name__ == '__main__':
    sys.exit(unittest.main())
