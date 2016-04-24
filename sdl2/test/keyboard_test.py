import sys
import unittest
from .. import SDL_Init, SDL_Quit, SDL_QuitSubSystem, SDL_INIT_VIDEO
from .. import rect, keyboard, scancode, keycode, video
from ctypes import c_int, cast, POINTER

byteify = lambda x: x.encode("utf-8")


class SDLKeyboardTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(SDL_INIT_VIDEO)

    def tearDown(self):
        SDL_QuitSubSystem(SDL_INIT_VIDEO)
        SDL_Quit()

    def test_SDL_Keysym(self):
        keysym = keyboard.SDL_Keysym()
        self.assertEqual(keysym.scancode, 0)
        self.assertEqual(keysym.sym, 0)
        self.assertEqual(keysym.mod, 0)

        keysym = keyboard.SDL_Keysym(1, 2, 3, ord("b"))
        self.assertEqual(keysym.scancode, 1)
        self.assertEqual(keysym.sym, 2)
        self.assertEqual(keysym.mod, 3)

        uval = "\u0220"
        if sys.version_info[0] < 3:
            uval = unichr(8224)
        keysym = keyboard.SDL_Keysym(17, 32, 88, ord(uval))
        self.assertEqual(keysym.scancode, 17)
        self.assertEqual(keysym.sym, 32)
        self.assertEqual(keysym.mod, 88)

    def test_SDL_GetKeyboardFocus(self):
        # window = keyboard.SDL_GetKeyboardFocus()
        # TODO: x
        # self.assertEqual(window, None)
        rwin = video.SDL_CreateWindow(b"test", 10, 10, 10, 10, 0)
        window = keyboard.SDL_GetKeyboardFocus()
        if window:
            self.assertEqual(video.SDL_GetWindowID(window),
                             video.SDL_GetWindowID(rwin))
        video.SDL_DestroyWindow(rwin)

        window = keyboard.SDL_GetKeyboardFocus()
        # TODO: x
        # self.assertEqual(window, None)

    def test_SDL_GetKeyboardState(self):
        states = (c_int * scancode.SDL_NUM_SCANCODES)()
        keyboard.SDL_GetKeyboardState(cast(states, POINTER(c_int)))
        self.assertEqual(len(states), scancode.SDL_NUM_SCANCODES)
        # TODO: x
        # for state in states:
        #    self.assertEqual(state, 0)

    def test_SDL_GetKeyFromName(self):
        for x in range(26):  # a-z
            key = keyboard.SDL_GetKeyFromName(byteify(chr(x + 97)))
            self.assertEqual(key, x + 97)

        for x in range(10):
            key = keyboard.SDL_GetKeyFromName(("%d" % x).encode("utf-8"))
            self.assertEqual(key, 48 + x)

        val = keyboard.SDL_GetKeyFromName(byteify(repr(self)))
        self.assertEqual(val, keycode.SDLK_UNKNOWN)

    def test_SDL_GetKeyFromScancode(self):
        p = 0
        for x in (scancode.SDL_SCANCODE_A,
                  scancode.SDL_SCANCODE_B,
                  scancode.SDL_SCANCODE_C):
            key = keyboard.SDL_GetKeyFromScancode(x)
            self.assertEqual(key, p + 97)
            p += 1

        p = 0
        for x in range(scancode.SDL_SCANCODE_1, scancode.SDL_SCANCODE_0):
            key = keyboard.SDL_GetKeyFromScancode(x)
            self.assertEqual(key, 49 + p)
            p += 1

        # self.assertRaises(TypeError, keyboard.get_key_from_scancode, self)
        # self.assertRaises(ValueError, keyboard.get_key_from_scancode, "Test")
        # self.assertRaises(TypeError, keyboard.get_key_from_scancode, None)

    def test_SDL_GetKeyName(self):
        x = 65  # SDL maps everything against upper-case letters
        for key in range(ord('a'), ord('z')):
            ch = chr(x)
            name = keyboard.SDL_GetKeyName(key)
            self.assertEqual(name, byteify(ch))
            x += 1

    def test_SDL_GetSetModState(self):
        initial = keyboard.SDL_GetModState()
        for state in(keycode.KMOD_NUM | keycode.KMOD_CAPS | keycode.KMOD_MODE,
                      keycode.KMOD_NUM | keycode.KMOD_CAPS,
                      keycode.KMOD_CAPS):
            keyboard.SDL_SetModState(state)
            self.assertEqual(keyboard.SDL_GetModState(), state)

        state = keycode.KMOD_NUM
        keyboard.SDL_SetModState(state)
        self.assertEqual(keyboard.SDL_GetModState(), state)

        keyboard.SDL_SetModState(initial)
        self.assertEqual(keyboard.SDL_GetModState(), initial)

    def test_SDL_GetScancodeFromKey(self):
        codes = range(scancode.SDL_SCANCODE_1, scancode.SDL_SCANCODE_0)
        xoff = 0
        for key in range(ord('1'), ord('0')):
            code = keyboard.SDL_GetScancodeFromKey(key)
            self.assertEqual(code, codes[xoff])
            xoff += 1

        key = keyboard.SDL_GetScancodeFromKey(477)
        self.assertEqual(key, scancode.SDL_SCANCODE_UNKNOWN)

        # self.assertRaises(TypeError, keyboard.get_scancode_from_key, None)
        # self.assertRaises(ValueError, keyboard.get_scancode_from_key, "Test")
        # self.assertRaises(TypeError, keyboard.get_scancode_from_key, self)

    def test_SDL_GetScancodeFromName(self):
        codes = range(scancode.SDL_SCANCODE_A, scancode.SDL_SCANCODE_Z)
        xoff = 0
        for key in range(ord('a'), ord('z')):
            ch = chr(key)
            code = keyboard.SDL_GetScancodeFromName(byteify(ch))
            self.assertEqual(code, codes[xoff])
            xoff += 1

        key = keyboard.SDL_GetScancodeFromName(b"")
        self.assertEqual(key, scancode.SDL_SCANCODE_UNKNOWN)

        key = keyboard.SDL_GetScancodeFromName(None)
        self.assertEqual(key, scancode.SDL_SCANCODE_UNKNOWN)

        key = keyboard.SDL_GetScancodeFromName(b"Test")
        self.assertEqual(key, scancode.SDL_SCANCODE_UNKNOWN)

        key = keyboard.SDL_GetScancodeFromName(byteify(repr(self)))
        self.assertEqual(key, scancode.SDL_SCANCODE_UNKNOWN)

    def test_SDL_GetScancodeName(self):
        names = range(ord('A'), ord('Z'))
        xoff = 0
        for code in range(scancode.SDL_SCANCODE_A, scancode.SDL_SCANCODE_Z):
            name = keyboard.SDL_GetScancodeName(code)
            self.assertEqual(name, byteify(chr(names[xoff])))
            xoff += 1

        name = keyboard.SDL_GetScancodeName(0)
        self.assertEqual(name, b"")

        # self.assertRaises(ValueError, keyboard.SDL_GetScancodeName, -22)
        # self.assertRaises(ValueError, keyboard.SDL_GetScancodeName,
        #                   scancode.SDL_NUM_SCANCODES)

        # self.assertRaises(TypeError, keyboard.get_scancode_from_key, None)
        # self.assertRaises(ValueError, keyboard.get_scancode_from_key, "Test")
        # self.assertRaises(TypeError, keyboard.get_scancode_from_key, self)

    def test_SDL_SetTextInputRect(self):
        # TODO: this test is a bit pointless
        coords = [(0, 0, 0, 0), (-10, -70, 3, 6), (10, 10, 10, 10)]
        for x, y, w, h in coords:
            r = rect.SDL_Rect(x, y, w, h)
            keyboard.SDL_SetTextInputRect(r)
        keyboard.SDL_SetTextInputRect(rect.SDL_Rect())

    @unittest.skip("not implemented")
    def test_SDL_StartTextInput(self):
        keyboard.SDL_StartTextInput()

    @unittest.skip("not implemented")
    def test_SDL_StopTextInput(self):
        keyboard.SDL_StopTextInput()

if __name__ == '__main__':
    sys.exit(unittest.main())
