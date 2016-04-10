import sys
import unittest
from .. import platform


class SDLPlatformTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def test_SDL_GetPlatform(self):
        retval = platform.SDL_GetPlatform()
        if sys.platform in ("win32", "cygwin"):
            self.assertEqual(retval, b"Windows")
        elif sys.platform.startswith("linux"):
            self.assertEqual(retval, b"Linux")
        elif sys.platform.startswith("freebsd"):
            self.assertEqual(retval, b"FreeBSD")
        elif sys.platform.startswith("darwin"):
            self.assertEqual(retval, b"Mac OS X")
        # Do not check others atm, since we are unsure about what Python will
        # return here.


if __name__ == '__main__':
    sys.exit(unittest.main())
