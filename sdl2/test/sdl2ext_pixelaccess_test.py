import sys
import pytest
from sdl2 import ext as sdl2ext

try:
    import numpy
    _HASNUMPY = True
except:
    _HASNUMPY = False


class TestSDL2ExtPixelAccess(object):
    __tags__ = ["sdl", "sdl2ext"]

    @classmethod
    def setup_class(cls):
        try:
            sdl2ext.init()
        except sdl2ext.SDLError:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        sdl2ext.quit()

    @pytest.mark.skipif(hasattr(sys, "pypy_version_info"),
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_PixelView(self):
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        sprite = factory.create_sprite(size=(10, 10), bpp=32)
        view = sdl2ext.PixelView(sprite)
        view[1] = (0xAABBCCDD,) * 10
        rcolor = sdl2ext.prepare_color(0xAABBCCDD, sprite)
        for index, row in enumerate(view):
            if index == 1:
                for col in row:
                    assert col == rcolor
            else:
                for col in row:
                    assert col == 0x0

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(not _HASNUMPY, reason="numpy module is not supported")
    def test_pixels2d(self):
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        sprite = factory.create_sprite(size=(5, 10), bpp=32,
                                       masks=(0xFF000000, 0x00FF0000,
                                              0x0000FF00, 0x000000FF))
        sdl2ext.fill(sprite, 0x01, (2, 2, 2, 2))
        nparray = sdl2ext.pixels2d(sprite)

    @pytest.mark.skipif(hasattr(sys, "pypy_version_info"),
        reason="PyPy's ctypes can't do byref(value, offset)")
    @pytest.mark.skipif(not _HASNUMPY, reason="numpy module is not supported")
    def test_pixels3d(self):
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        sprite = factory.create_sprite(size=(5, 10), bpp=32,
                                       masks=(0xFF000000, 0x00FF0000,
                                              0x0000FF00, 0x000000FF))
        sdl2ext.fill(sprite, 0xAABBCCDD, (1, 2, 3, 4))
        nparray = sdl2ext.pixels3d(sprite)
        for x in range(1, 4):
            for y in range(2, 6):
                assert numpy.all([nparray[x, y],
                                           [0xAA, 0xBB, 0xCC, 0xDD]])
        assert not numpy.all([nparray[0, 0], [0xAA, 0xBB, 0xCC, 0xDD]])
        assert not numpy.all([nparray[1, 0], [0xAA, 0xBB, 0xCC, 0xDD]])
        assert not numpy.all([nparray[0, 1], [0xAA, 0xBB, 0xCC, 0xDD]])
        assert not numpy.all([nparray[3, 6], [0xAA, 0xBB, 0xCC, 0xDD]])
        assert not numpy.all([nparray[4, 6], [0xAA, 0xBB, 0xCC, 0xDD]])
