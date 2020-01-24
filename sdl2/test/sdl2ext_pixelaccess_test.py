import os
import sys
import pytest
from sdl2 import ext as sdl2ext
from sdl2.ext import color
from sdl2 import surface, pixels

try:
    import numpy
    _HASNUMPY = True
except:
    _HASNUMPY = False


class TestSDL2ExtPixelAccess(object):
    __tags__ = ["sdl", "sdl2ext"]

    @classmethod
    def setup_class(cls):
        cls.testfile = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "resources", "surfacetest.bmp"
        )
        try:
            sdl2ext.init()
        except sdl2ext.SDLError:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        sdl2ext.quit()


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

    @pytest.mark.skipif(not _HASNUMPY, reason="numpy module is not supported")
    def test_pixels2d(self):
        colors = {
            'red': color.Color(255, 0, 0, 255),
            'blue': color.Color(0, 0, 255, 255),
            'black': color.Color(0, 0, 0, 255),
            'white': color.Color(255, 255, 255, 255)
        }
        # Import test image, convert to RGBA, and open pixels2d view
        imgsurf = surface.SDL_LoadBMP(self.testfile.encode("utf-8"))
        with pytest.warns(sdl2ext.compat.ExperimentalWarning):
            nparray = sdl2ext.pixels2d(imgsurf.contents, transpose=False)
        assert nparray.shape == (32, 32)
        # Test different coordinates on surface
        assert color.ARGB(nparray[0][0]) == colors['red']
        assert color.ARGB(nparray[0][16]) == colors['blue']
        assert color.ARGB(nparray[0][31]) == colors['white']
        assert color.ARGB(nparray[31][31]) == colors['black']
        # Try modifying surface, test if changes persist 
        nparray[31][0] = 0xFF808080 # medium grey in ARGB
        with pytest.warns(sdl2ext.compat.ExperimentalWarning):
            nparray2 = sdl2ext.pixels2d(imgsurf.contents, transpose=False)
        assert nparray2[31][0] == 0xFF808080


    @pytest.mark.skipif(not _HASNUMPY, reason="numpy module is not supported")
    def test_pixels3d(self):
        colors = {
            'red': color.Color(255, 0, 0, 255),
            'blue': color.Color(0, 0, 255, 255),
            'black': color.Color(0, 0, 0, 255),
            'white': color.Color(255, 255, 255, 255)
        }
        rgba = pixels.SDL_PIXELFORMAT_ABGR8888
        # Import test image, convert to RGBA, and open pixels3d view
        imgsurf = surface.SDL_LoadBMP(self.testfile.encode("utf-8"))
        imgsurf = surface.SDL_ConvertSurfaceFormat(imgsurf.contents, rgba, 0)
        with pytest.warns(sdl2ext.compat.ExperimentalWarning):
            nparray = sdl2ext.pixels3d(imgsurf.contents, transpose=False)
        assert nparray.shape == (32, 32, 4)
        # Test different coordinates on surface
        assert color.Color(*nparray[0][0]) == colors['red']
        assert color.Color(*nparray[0][16]) == colors['blue']
        assert color.Color(*nparray[0][31]) == colors['white']
        assert color.Color(*nparray[31][31]) == colors['black']
        # Try modifying surface, test if changes persist 
        grey = [128, 128, 128, 255]
        nparray[31][0][:] = grey
        with pytest.warns(sdl2ext.compat.ExperimentalWarning):
            nparray2 = sdl2ext.pixels3d(imgsurf.contents, transpose=False)
        assert color.Color(*nparray2[31][0]) == color.Color(*grey)
