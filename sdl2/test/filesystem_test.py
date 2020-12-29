import os
import sys
import pytest
from ctypes import cast, c_char_p, addressof
from sdl2 import filesystem, SDL_free


class TestSDLFileSystem(object):
    __tags__ = ["sdl"]

    def test_SDL_GetBasePath(self):
        path = filesystem.SDL_GetBasePath()
        path = path.decode("utf-8")
        if sys.version_info[0] < 3:
            assert u"python" in path.lower()
        else:
            execprefix = sys.base_exec_prefix
            assert execprefix.lower() in path.lower()

    def test_SDL_GetPrefPath(self):
        path = filesystem.SDL_GetPrefPath(b"OrgName", b"AppName")
        path = path.decode("utf-8")
        assert "OrgName" in path
        assert "AppName" in path
