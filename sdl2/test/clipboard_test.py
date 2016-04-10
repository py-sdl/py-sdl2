import sys
import unittest
from .. import SDL_Init, SDL_Quit, SDL_InitSubSystem, SDL_INIT_EVERYTHING
from .. import clipboard
from ..stdinc import SDL_TRUE
from .util.testutils import interactive, doprint


def is_win_or_mac():
    return sys.platform in ("win32", "cygwin", "darwin")


class SDLClipboardTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(SDL_INIT_EVERYTHING)

    def tearDown(self):
        SDL_Quit()

    @unittest.skipIf(not is_win_or_mac(), "we would need a SDL window")
    @interactive()
    def test_SDL_HasClipboardText(self):
        doprint("Please put some text on the clipboard")
        self.assertEqual(clipboard.SDL_HasClipboardText(), SDL_TRUE)

    @unittest.skipIf(not is_win_or_mac(), "we would need a SDL window")
    @interactive("Does the shown value match the clipboard content?")
    def test_SDL_GetClipboardText(self):
        doprint("Please put some text on the clipboard")
        retval = clipboard.SDL_GetClipboardText()
        doprint("Clipboard content: '%s'" % retval)

    @unittest.skipIf(not is_win_or_mac(), "we would need a SDL window")
    def test_SDL_SetClipboardText(self):
        self.assertEquals(clipboard.SDL_SetClipboardText(b"Test content"), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, b"Test content")

        self.assertEquals(clipboard.SDL_SetClipboardText(b""), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, b"")

        self.assertEquals(clipboard.SDL_SetClipboardText(b"Test content"), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, b"Test content")

        self.assertEquals(clipboard.SDL_SetClipboardText(None), 0)
        retval = clipboard.SDL_GetClipboardText()
        self.assertEqual(retval, b"")


if __name__ == '__main__':
    sys.exit(unittest.main())
