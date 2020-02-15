import sys
import ctypes
import pytest
from sdl2 import version, __version__, version_info


class TestSDLVersion(object):
    __tags__ = ["sdl"]

    def test___version__(self):
        assert __version__ == "0.9.8"

    def test_version_info(self):
        assert version_info == (0, 9, 8, "")

    def test_SDL_version(self):
        v = version.SDL_version(0, 0, 0)
        assert v.major == 0
        assert v.minor == 0
        assert v.patch == 0

    def test_SDL_GetVersion(self):
        v = version.SDL_version()
        version.SDL_GetVersion(ctypes.byref(v))
        assert type(v) == version.SDL_version
        assert v.major == 2
        assert v.minor == 0
        assert v.patch >= 5

    def test_SDL_VERSIONNUM(self):
        assert version.SDL_VERSIONNUM(1, 2, 3) == 1203
        assert version.SDL_VERSIONNUM(4, 5, 6) == 4506
        assert version.SDL_VERSIONNUM(2, 0, 0) == 2000
        assert version.SDL_VERSIONNUM(17, 42, 3) == 21203

    def test_SDL_VERSION_ATLEAST(self):
        assert version.SDL_VERSION_ATLEAST(1, 2, 3)
        assert version.SDL_VERSION_ATLEAST(2, 0, 0)
        assert version.SDL_VERSION_ATLEAST(2, 0, 1)
        assert not version.SDL_VERSION_ATLEAST(2, 0, 100)

    def test_SDL_GetRevision(self):
        assert version.SDL_GetRevision()[0:3] == b"hg-"

    def test_SDL_GetRevisionNumber(self):
        if sys.platform in ("win32",):
            # HG tip on Win32 does not set any revision number
            assert version.SDL_GetRevisionNumber() >= 0
        else:
            assert version.SDL_GetRevisionNumber() >= 7000
