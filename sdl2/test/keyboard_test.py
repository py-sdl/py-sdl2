import sys
import pytest
from ctypes import c_int, cast, POINTER
from sdl2 import SDL_Init, SDL_Quit, SDL_QuitSubSystem, SDL_INIT_VIDEO
from sdl2 import rect, keyboard, scancode, keycode, video

byteify = lambda x: x.encode("utf-8")


class TestSDLKeyboard(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        if SDL_Init(SDL_INIT_VIDEO) != 0:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        SDL_QuitSubSystem(SDL_INIT_VIDEO)
        SDL_Quit()

    def test_SDL_Keysym(self):
        keysym = keyboard.SDL_Keysym()
        assert keysym.scancode == 0
        assert keysym.sym == 0
        assert keysym.mod == 0

        keysym = keyboard.SDL_Keysym(1, 2, 3, ord("b"))
        assert keysym.scancode == 1
        assert keysym.sym == 2
        assert keysym.mod == 3

        uval = "\u0220"
        if sys.version_info[0] < 3:
            uval = unichr(8224)
        keysym = keyboard.SDL_Keysym(17, 32, 88, ord(uval))
        assert keysym.scancode == 17
        assert keysym.sym == 32
        assert keysym.mod == 88

    @pytest.mark.skipif(sys.platform == "darwin", reason="crashes on OS X")
    def test_SDL_GetKeyboardFocus(self):
        # window = keyboard.SDL_GetKeyboardFocus()
        # TODO: x
        # self.assertEqual(window, None)
        rwin = video.SDL_CreateWindow(b"test", 10, 10, 10, 10, 0)
        window = keyboard.SDL_GetKeyboardFocus()
        if window:
            assert video.SDL_GetWindowID(window) == video.SDL_GetWindowID(rwin)
        video.SDL_DestroyWindow(rwin)

        window = keyboard.SDL_GetKeyboardFocus()
        # TODO: x
        # self.assertEqual(window, None)

    def test_SDL_GetKeyboardState(self):
        states = (c_int * scancode.SDL_NUM_SCANCODES)()
        keyboard.SDL_GetKeyboardState(cast(states, POINTER(c_int)))
        assert len(states) == scancode.SDL_NUM_SCANCODES
        # TODO: x
        # for state in states:
        #    self.assertEqual(state, 0)

    def test_SDL_GetKeyFromName(self):
        for x in range(26):  # a-z
            key = keyboard.SDL_GetKeyFromName(byteify(chr(x + 97)))
            assert key == x + 97

        for x in range(10):
            key = keyboard.SDL_GetKeyFromName(("%d" % x).encode("utf-8"))
            assert key == 48 + x

        val = keyboard.SDL_GetKeyFromName(byteify(repr(self)))
        assert val == keycode.SDLK_UNKNOWN

    def test_SDL_GetKeyFromScancode(self):
        p = 0
        for x in (scancode.SDL_SCANCODE_A,
                  scancode.SDL_SCANCODE_B,
                  scancode.SDL_SCANCODE_C):
            key = keyboard.SDL_GetKeyFromScancode(x)
            assert key == p + 97
            p += 1

        p = 0
        for x in range(scancode.SDL_SCANCODE_1, scancode.SDL_SCANCODE_0):
            key = keyboard.SDL_GetKeyFromScancode(x)
            assert key == 49 + p
            p += 1

    def test_SDL_GetKeyName(self):
        x = 65  # SDL maps everything against upper-case letters
        for key in range(ord('a'), ord('z')):
            ch = chr(x)
            name = keyboard.SDL_GetKeyName(key)
            assert name == byteify(ch)
            x += 1

    def test_SDL_GetSetModState(self):
        initial = keyboard.SDL_GetModState()
        for state in(keycode.KMOD_NUM | keycode.KMOD_CAPS | keycode.KMOD_MODE,
                      keycode.KMOD_NUM | keycode.KMOD_CAPS,
                      keycode.KMOD_CAPS):
            keyboard.SDL_SetModState(state)
            assert keyboard.SDL_GetModState() == state

        state = keycode.KMOD_NUM
        keyboard.SDL_SetModState(state)
        assert keyboard.SDL_GetModState() == state

        keyboard.SDL_SetModState(initial)
        assert keyboard.SDL_GetModState() == initial

    def test_SDL_GetScancodeFromKey(self):
        codes = range(scancode.SDL_SCANCODE_1, scancode.SDL_SCANCODE_0)
        xoff = 0
        for key in range(ord('1'), ord('0')):
            code = keyboard.SDL_GetScancodeFromKey(key)
            assert code == codes[xoff]
            xoff += 1

        key = keyboard.SDL_GetScancodeFromKey(477)
        assert key == scancode.SDL_SCANCODE_UNKNOWN

    def test_SDL_GetScancodeFromName(self):
        codes = range(scancode.SDL_SCANCODE_A, scancode.SDL_SCANCODE_Z)
        xoff = 0
        for key in range(ord('a'), ord('z')):
            ch = chr(key)
            code = keyboard.SDL_GetScancodeFromName(byteify(ch))
            assert code == codes[xoff]
            xoff += 1

        key = keyboard.SDL_GetScancodeFromName(b"")
        assert key == scancode.SDL_SCANCODE_UNKNOWN

        key = keyboard.SDL_GetScancodeFromName(None)
        assert key == scancode.SDL_SCANCODE_UNKNOWN

        key = keyboard.SDL_GetScancodeFromName(b"Test")
        assert key == scancode.SDL_SCANCODE_UNKNOWN

        key = keyboard.SDL_GetScancodeFromName(byteify(repr(self)))
        assert key == scancode.SDL_SCANCODE_UNKNOWN

    def test_SDL_GetScancodeName(self):
        names = range(ord('A'), ord('Z'))
        xoff = 0
        for code in range(scancode.SDL_SCANCODE_A, scancode.SDL_SCANCODE_Z):
            name = keyboard.SDL_GetScancodeName(code)
            assert name == byteify(chr(names[xoff]))
            xoff += 1

        name = keyboard.SDL_GetScancodeName(0)
        assert name == b""

        # self.assertRaises(ValueError, keyboard.SDL_GetScancodeName, -22)
        # self.assertRaises(ValueError, keyboard.SDL_GetScancodeName,
        #                   scancode.SDL_NUM_SCANCODES)

    def test_SDL_SetTextInputRect(self):
        # TODO: this test is a bit pointless
        coords = [(0, 0, 0, 0), (-10, -70, 3, 6), (10, 10, 10, 10)]
        for x, y, w, h in coords:
            r = rect.SDL_Rect(x, y, w, h)
            keyboard.SDL_SetTextInputRect(r)
        keyboard.SDL_SetTextInputRect(rect.SDL_Rect())

    @pytest.mark.skip("not implemented")
    def test_SDL_StartTextInput(self):
        keyboard.SDL_StartTextInput()

    @pytest.mark.skip("not implemented")
    def test_SDL_StopTextInput(self):
        keyboard.SDL_StopTextInput()
