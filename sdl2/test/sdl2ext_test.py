import sys
import pytest
from sdl2 import ext as sdl2ext
from sdl2 import SDL_WasInit, SDL_INIT_VIDEO, SDL_FlushEvent, SDL_USEREVENT, \
    SDL_FIRSTEVENT, SDL_LASTEVENT, SDL_Event, SDL_UserEvent, SDL_PushEvent


class TestSDL2Ext(object):
    __tags__ = ["sdl", "sdl2ext"]

    def test_init_quit(self):
        try:
            sdl2ext.init()
        except sdl2ext.SDLError:
            raise pytest.skip('Video subsystem not supported')
        assert SDL_WasInit(SDL_INIT_VIDEO) == SDL_INIT_VIDEO
        sdl2ext.quit()
        assert SDL_WasInit(SDL_INIT_VIDEO) != SDL_INIT_VIDEO
        sdl2ext.init()
        sdl2ext.init()
        sdl2ext.init()
        assert SDL_WasInit(SDL_INIT_VIDEO) == SDL_INIT_VIDEO
        sdl2ext.quit()
        assert SDL_WasInit(SDL_INIT_VIDEO) != SDL_INIT_VIDEO
        sdl2ext.quit()
        sdl2ext.quit()
        sdl2ext.quit()
        assert SDL_WasInit(SDL_INIT_VIDEO) != SDL_INIT_VIDEO

    def test_get_events(self):
        try:
            sdl2ext.init()
        except sdl2ext.SDLError:
            raise pytest.skip('Video subsystem not supported')
        SDL_FlushEvent(SDL_FIRSTEVENT, SDL_LASTEVENT)
        for x in range(10):
            event = SDL_Event()
            event.type = SDL_USEREVENT + 1
            event.user = SDL_UserEvent(type=event.type, timestamp=0,
                                       windowID=0, code=0)
            SDL_PushEvent(event)
        results = sdl2ext.get_events()
        assert len(results) == 10
        for ev in results:
            assert ev.type == (SDL_USEREVENT + 1)

    def test_get_events_issue_6(self):
        try:
            sdl2ext.init()
        except sdl2ext.SDLError:
            raise pytest.skip('Video subsystem not supported')
        SDL_FlushEvent(SDL_FIRSTEVENT, SDL_LASTEVENT)
        for x in range(12):
            event = SDL_Event()
            event.type = SDL_USEREVENT + x
            event.user = SDL_UserEvent(type=event.type, timestamp=0,
                                       windowID=0, code=0)
            SDL_PushEvent(event)
        results = sdl2ext.get_events()
        for idx, r in enumerate(results):
            assert idx == r.type - SDL_USEREVENT

    def test_TestEventProcessor(self):
        proc = sdl2ext.TestEventProcessor()
        assert isinstance(proc, sdl2ext.TestEventProcessor)
