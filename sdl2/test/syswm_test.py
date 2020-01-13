import sys
import pytest
import ctypes
from sdl2.stdinc import SDL_TRUE
from sdl2 import video, syswm, version


class TestSDLSysWM(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        if video.SDL_VideoInit(None) != 0:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        video.SDL_VideoQuit()

    def test_SDL_GetWindowWMInfo(self):
        if video.SDL_GetCurrentVideoDriver() == b"dummy":
            pytest.skip("cannot retrieve WM information for the dummy video driver")

        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                        video.SDL_WINDOW_HIDDEN)
        wminfo = syswm.SDL_SysWMinfo()
        version.SDL_VERSION(wminfo.version)
        ret = syswm.SDL_GetWindowWMInfo(window, ctypes.byref(wminfo))
        assert ret == SDL_TRUE
        if sys.platform in ("win32", "cygwin"):
            assert wminfo.subsystem == syswm.SDL_SYSWM_WINDOWS
        elif sys.platform.startswith("linux"):
            assert wminfo.subsystem in \
                   (syswm.SDL_SYSWM_X11, syswm.SDL_SYSWM_DIRECTFB)
        elif sys.platform.startswith("freebsd"):
            assert wminfo.subsystem in \
                   (syswm.SDL_SYSWM_X11, syswm.SDL_SYSWM_DIRECTFB)
        elif sys.platform.startswith("darwin"):
            assert wminfo.subsystem == syswm.SDL_SYSWM_COCOA
        video.SDL_DestroyWindow(window)
        # TODO: not sure, what to test here specifically
