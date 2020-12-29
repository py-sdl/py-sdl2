import sys
from ctypes import c_int, byref
import pytest
import sdl2
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_VIDEO
from sdl2 import metal, video, error

macos = sys.platform == "darwin"

# TODO: Add more complete tests with pyobjc


class TestSDLMetal(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        if SDL_Init(SDL_INIT_VIDEO) != 0:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    @pytest.mark.xfail(reason="Metal not supported on all macs")
    @pytest.mark.skipif(sdl2.dll.version < 2012 or not macos, reason="not available")
    def test_SDL_Metal_CreateDestroyView(self):
        error.SDL_ClearError()
        flags = video.SDL_WINDOW_HIDDEN | video.SDL_WINDOW_METAL
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flags)
        assert isinstance(window.contents, video.SDL_Window)
        view = metal.SDL_Metal_CreateView(window)
        err = error.SDL_GetError()
        if len(err):
            print("Metal Error: '{0}'".format(err.decode('utf-8')))
        assert view  # Verify pointer is not null
        metal.SDL_Metal_DestroyView(view)
        video.SDL_DestroyWindow(window)

    @pytest.mark.xfail(reason="Metal not supported on all macs")
    @pytest.mark.skipif(sdl2.dll.version < 2014 or not macos, reason="not available")
    def test_SDL_Metal_GetLayer(self):
        flags = video.SDL_WINDOW_HIDDEN | video.SDL_WINDOW_METAL
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flags)
        assert isinstance(window.contents, video.SDL_Window)
        view = metal.SDL_Metal_CreateView(window)
        assert view  # Verify pointer is not null
        layer = metal.SDL_Metal_GetLayer(view)
        assert layer  # Verify pointer is not null
        metal.SDL_Metal_DestroyView(view)
        video.SDL_DestroyWindow(window)

    @pytest.mark.xfail(reason="Metal not supported on all macs")
    @pytest.mark.skipif(sdl2.dll.version < 2014 or not macos, reason="not available")
    def test_SDL_Metal_GetDrawableSize(self):
        flags = video.SDL_WINDOW_HIDDEN | video.SDL_WINDOW_METAL
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flags)
        assert isinstance(window.contents, video.SDL_Window)
        view = metal.SDL_Metal_CreateView(window)
        assert view  # Verify pointer is not null
        w, h = c_int(0), c_int(0)
        metal.SDL_Metal_GetDrawableSize(window, byref(w), byref(h))
        assert w.value == 10 and h.value == 10
        metal.SDL_Metal_DestroyView(view)
        video.SDL_DestroyWindow(window)
