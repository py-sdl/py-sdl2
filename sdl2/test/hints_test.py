import sys
import pytest
from ctypes import cast, c_char_p
from sdl2 import SDL_Init, SDL_Quit, SDL_QuitSubSystem, SDL_INIT_EVERYTHING
from sdl2 import hints
from sdl2.stdinc import SDL_TRUE, SDL_FALSE

class TestSDLHints(object):
    __tags__ = ["sdl"]

    def setup_method(self):
        SDL_Init(SDL_INIT_EVERYTHING)

    def teardown_method(self):
        SDL_QuitSubSystem(SDL_INIT_EVERYTHING)
        SDL_Quit()

    def test_SDL_ClearHints(self):
        assert hints.SDL_SetHint(b"TEST", b"32") == 1
        assert hints.SDL_GetHint(b"TEST") == b"32"
        hints.SDL_ClearHints()
        assert hints.SDL_GetHint(b"TEST") == None

    def test_SDL_GetHint(self):
        assert hints.SDL_SetHint(b"TEST", b"32") == 1
        assert hints.SDL_GetHint(b"TEST") == b"32"
        assert hints.SDL_SetHint(hints.SDL_HINT_ALLOW_TOPMOST, b"true") == 1
        assert hints.SDL_GetHint(hints.SDL_HINT_ALLOW_TOPMOST) == b"true"

    def test_SDL_SetHint(self):
        assert hints.SDL_SetHint(b"TEST", b"32") == 1
        assert hints.SDL_GetHint(b"TEST") == b"32"
        assert hints.SDL_SetHint(b"TEST", b"abcdef") == 1
        assert hints.SDL_GetHint(b"TEST") == b"abcdef"
        assert hints.SDL_SetHint(b"", b"hi") == 1
        assert hints.SDL_GetHint(b"") == b"hi"

    def test_SDL_SetHintWithPriority(self):
        assert hints.SDL_SetHintWithPriority(
                        b"TEST", b"32", hints.SDL_HINT_DEFAULT) == 1
        assert hints.SDL_GetHint(b"TEST") == b"32"
        assert hints.SDL_SetHintWithPriority(
                        b"TEST", b"abcdef", hints.SDL_HINT_NORMAL) == 1
        assert hints.SDL_GetHint(b"TEST") == b"abcdef"
        assert hints.SDL_SetHintWithPriority(
                        b"", b"hi", hints.SDL_HINT_OVERRIDE) == 1
        assert hints.SDL_GetHint(b"") == b"hi"
        assert hints.SDL_SetHintWithPriority(
                        b"", b"bye", hints.SDL_HINT_NORMAL) == 0

    def test_SDL_GetHintBoolean(self):
        assert hints.SDL_SetHint(b"TEST", b"32") == 1
        assert hints.SDL_GetHintBoolean(b"TEST", SDL_TRUE) == SDL_TRUE
        assert hints.SDL_GetHintBoolean(b"TEST", SDL_FALSE) == SDL_TRUE
        assert hints.SDL_GetHintBoolean(b"TEST2", SDL_FALSE) != SDL_TRUE

    def test_SDL_AddDelHintCallback(self):
        calls = []
        def callback(userdata, name, oldval, newval):
            data = cast(userdata, c_char_p)
            calls.append((data.value, name, oldval, newval))
        hintcb = hints.SDL_HintCallback(callback)
        udata = c_char_p(b"banana")
        hints.SDL_AddHintCallback(hints.SDL_HINT_ALLOW_TOPMOST, hintcb,
                                  udata)
        # SDL_AddHintCallback invokes the callback once.
        assert len(calls) == 1
        assert calls[0] == (b"banana", hints.SDL_HINT_ALLOW_TOPMOST,
                                    None, None)
        hints.SDL_SetHint(hints.SDL_HINT_ALLOW_TOPMOST, b"true")
        assert len(calls) == 2
        assert calls[1] == (b"banana", hints.SDL_HINT_ALLOW_TOPMOST,
                                    None, b"true")
        hints.SDL_DelHintCallback(hints.SDL_HINT_ALLOW_TOPMOST, hintcb,
                                  udata)
        hints.SDL_SetHint(hints.SDL_HINT_ALLOW_TOPMOST, b"false")
        assert len(calls) == 2
