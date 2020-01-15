import os
import sys
import unittest
from ctypes import cast, c_char_p, addressof
from sdl2 import filesystem, SDL_free


class SDLFileSystemTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def test_SDL_GetBasePath(self):
        execprefix = sys.exec_prefix
        path = filesystem.SDL_GetBasePath()
        path = path.decode("utf-8")
        if sys.version_info[0] < 3:
            execprefix = unicode(execprefix)
        self.assertTrue(execprefix.lower() in path.lower())

    def test_SDL_GetPrefPath(self):
        path = filesystem.SDL_GetPrefPath(b"OrgName", b"AppName")
        path = path.decode("utf-8")
        self.assertTrue("OrgName" in path)
        self.assertTrue("AppName" in path)


if __name__ == '__main__':
    sys.exit(unittest.main())
