import sys
import pytest
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_EVERYTHING
from sdl2 import clipboard
from sdl2.stdinc import SDL_TRUE


def is_win_or_mac():
    return sys.platform in ("win32", "cygwin", "darwin")


class TestSDLClipboard(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        SDL_Init(SDL_INIT_EVERYTHING)

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    # @pytest.mark.skipif(not is_win_or_mac(), 
    #     reason="we would need a SDL window")
    # @interactive()
    # def test_SDL_HasClipboardText(self):
    #     doprint("Please put some text on the clipboard")
    #     self.assertEqual(clipboard.SDL_HasClipboardText(), SDL_TRUE)

    # @pytest.mark.skipif(not is_win_or_mac(), 
    #     reason="we would need a SDL window")
    # @interactive("Does the shown value match the clipboard content?")
    # def test_SDL_GetClipboardText(self):
    #     doprint("Please put some text on the clipboard")
    #     retval = clipboard.SDL_GetClipboardText()
    #     doprint("Clipboard content: '%s'" % retval)

    # @pytest.mark.skipif(not is_win_or_mac(), 
    #     reason="we would need a SDL window")
    # def test_SDL_SetClipboardText(self):
    #     self.assertEquals(clipboard.SDL_SetClipboardText(b"Test content"), 0)
    #     retval = clipboard.SDL_GetClipboardText()
    #     self.assertEqual(retval, b"Test content")

    #     self.assertEquals(clipboard.SDL_SetClipboardText(b""), 0)
    #     retval = clipboard.SDL_GetClipboardText()
    #     self.assertEqual(retval, b"")

    #     self.assertEquals(clipboard.SDL_SetClipboardText(b"Test content"), 0)
    #     retval = clipboard.SDL_GetClipboardText()
    #     self.assertEqual(retval, b"Test content")

    #     self.assertEquals(clipboard.SDL_SetClipboardText(None), 0)
    #     retval = clipboard.SDL_GetClipboardText()
    #     self.assertEqual(retval, b"")
