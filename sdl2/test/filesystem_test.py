import os
import sys
import unittest
from ctypes import cast, c_char_p, addressof
from .. import filesystem, SDL_free


class SDLFileSystemTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def test_SDL_GetBasePath(self):
        execpath = os.path.dirname(sys.executable) + os.sep
        path = filesystem.SDL_GetBasePath()
        ppath = cast(path, c_char_p).value
        self.assertEqual(execpath, ppath.decode("utf-8"))
        SDL_free(path)

    @unittest.skip("not implemented")
    def test_SDL_GetPrefPath(self):
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
