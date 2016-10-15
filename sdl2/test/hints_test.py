import sys
import unittest
from ctypes import cast, c_char_p
from .. import SDL_Init, SDL_Quit, SDL_QuitSubSystem, SDL_INIT_EVERYTHING
from .. import hints
from ..stdinc import SDL_TRUE, SDL_FALSE

class SDLHintsTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(SDL_INIT_EVERYTHING)

    def tearDown(self):
        SDL_QuitSubSystem(SDL_INIT_EVERYTHING)
        SDL_Quit()

    def test_SDL_ClearHints(self):
        self.assertEqual(hints.SDL_SetHint(b"TEST", b"32"), 1)
        self.assertEqual(hints.SDL_GetHint(b"TEST"), b"32")
        hints.SDL_ClearHints()
        self.assertEqual(hints.SDL_GetHint(b"TEST"), None)

    def test_SDL_GetHint(self):
        self.assertEqual(hints.SDL_SetHint(b"TEST", b"32"), 1)
        self.assertEqual(hints.SDL_GetHint(b"TEST"), b"32")
        self.assertEqual(hints.SDL_SetHint(hints.SDL_HINT_RENDER_DRIVER,
                                           b"dummy"), 1)
        self.assertEqual(hints.SDL_GetHint(hints.SDL_HINT_RENDER_DRIVER),
                         b"dummy")

    def test_SDL_SetHint(self):
        self.assertEqual(hints.SDL_SetHint(b"TEST", b"32"), 1)
        self.assertEqual(hints.SDL_GetHint(b"TEST"), b"32")
        self.assertEqual(hints.SDL_SetHint(b"TEST", b"abcdef"), 1)
        self.assertEqual(hints.SDL_GetHint(b"TEST"), b"abcdef")
        self.assertEqual(hints.SDL_SetHint(b"", b""), 1)
        self.assertEqual(hints.SDL_GetHint(b""), b"")

    def test_SDL_SetHintWithPriority(self):
        self.assertEqual(hints.SDL_SetHintWithPriority
                         (b"TEST", b"32", hints.SDL_HINT_DEFAULT), 1)
        self.assertEqual(hints.SDL_GetHint(b"TEST"), b"32")
        self.assertEqual(hints.SDL_SetHintWithPriority
                         (b"TEST", b"abcdef", hints.SDL_HINT_NORMAL), 1)
        self.assertEqual(hints.SDL_GetHint(b"TEST"), b"abcdef")
        self.assertEqual(hints.SDL_SetHintWithPriority
                         (b"", b"", hints.SDL_HINT_OVERRIDE), 1)
        self.assertEqual(hints.SDL_GetHint(b""), b"")


        # self.assertRaises(ValueError, hints.SDL_SetHintWithPriority,
        #                  "TEST", "123456789", 12)
        # self.assertRaises(ValueError, hints.SDL_SetHintWithPriority,
        #                  "TEST", "123456789", -78)
        # self.assertRaises(ValueError, hints.SDL_SetHintWithPriority,
        #                  "TEST", "123456789", None)
        # self.assertRaises(ValueError, hints.SDL_SetHintWithPriority,
        #                  "TEST", "123456789", "bananas")

    def test_SDL_GetHintBoolean(self):
        self.assertEqual(hints.SDL_SetHint(b"TEST", b"32"), 1)
        self.assertEqual(hints.SDL_GetHintBoolean(b"TEST", SDL_TRUE), SDL_TRUE)
        self.assertEqual(hints.SDL_GetHintBoolean(b"TEST", SDL_FALSE), SDL_TRUE)
        self.assertNotEqual(hints.SDL_GetHintBoolean(b"TEST2", SDL_FALSE), SDL_TRUE)

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
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0], (b"banana", hints.SDL_HINT_ALLOW_TOPMOST,
                                    None, None))
        hints.SDL_SetHint(hints.SDL_HINT_ALLOW_TOPMOST, b"true")
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[1], (b"banana", hints.SDL_HINT_ALLOW_TOPMOST,
                                    None, b"true"))
        hints.SDL_DelHintCallback(hints.SDL_HINT_ALLOW_TOPMOST, hintcb,
                                  udata)
        hints.SDL_SetHint(hints.SDL_HINT_ALLOW_TOPMOST, b"false")
        self.assertEqual(len(calls), 2)


if __name__ == '__main__':
    sys.exit(unittest.main())
