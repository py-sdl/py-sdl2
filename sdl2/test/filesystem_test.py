import os
import sys
import pytest
from ctypes import cast, c_char_p, addressof
from sdl2 import filesystem, SDL_free


class TestSDLFileSystem(object):
    __tags__ = ["sdl"]

    def test_SDL_GetBasePath(self):
        execprefix = sys.exec_prefix
        path = filesystem.SDL_GetBasePath()
        ppath = cast(path, c_char_p).value
        ppath = ppath.decode("utf-8")
        if sys.version_info[0] < 3:
            execprefix = unicode(execprefix)
        assert execprefix.lower() in ppath.lower()
        SDL_free(path)

    @pytest.mark.skip("not implemented")
    def test_SDL_GetPrefPath(self):
        pass
