import sys
import unittest
import ctypes
from ..stdinc import SDL_TRUE
from .. import video, syswm, version


class SDLSysWMTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        video.SDL_VideoInit(None)

    def tearDown(self):
        video.SDL_VideoQuit()

    def test_SDL_GetWindowWMInfo(self):
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                        video.SDL_WINDOW_HIDDEN)
        wminfo = syswm.SDL_SysWMinfo()
        version.SDL_VERSION(wminfo.version)
        ret = syswm.SDL_GetWindowWMInfo(window, ctypes.byref(wminfo))
        self.assertEqual(ret, SDL_TRUE)
        if sys.platform in ("win32", "cygwin"):
            self.assertEqual(wminfo.subsystem, syswm.SDL_SYSWM_WINDOWS)
        elif sys.platform.startswith("linux"):
            self.assertIn(wminfo.subsystem,
                          (syswm.SDL_SYSWM_X11, syswm.SDL_SYSWM_DIRECTFB))
        elif sys.platform.startswith("freebsd"):
            self.assertIn(wminfo.subsystem,
                          (syswm.SDL_SYSWM_X11, syswm.SDL_SYSWM_DIRECTFB))
        elif sys.platform.startswith("darwin"):
            self.assertEqual(wminfo.subsystem, syswm.SDL_SYSWM_COCOA)
        video.SDL_DestroyWindow(window)
        # TODO: not sure, what to test here specifically


if __name__ == '__main__':
    sys.exit(unittest.main())
