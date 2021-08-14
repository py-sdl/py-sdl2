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


colors = {
    'red': color.Color(255, 0, 0, 255),
    'blue': color.Color(0, 0, 255, 255),
    'black': color.Color(0, 0, 0, 255),
    'white': color.Color(255, 255, 255, 255)
}


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
        # Import test image and open pixel view
        imgsurf = surface.SDL_LoadBMP(self.testfile.encode("utf-8"))
        pxview = sdl2ext.PixelView(imgsurf.contents)

        # Test different coordinates on surface
        assert color.ARGB(pxview[0][0]) == colors['red']
        assert color.ARGB(pxview[0][16]) == colors['blue']
        assert color.ARGB(pxview[0][31]) == colors['white']
        assert color.ARGB(pxview[31][31]) == colors['black']

        # Try modifying surface, test if changes persist 
        pxview[31][0] = 0xFF808080 # medium grey in ARGB
        pxview2 = sdl2ext.PixelView(imgsurf)
        assert pxview2[31][0] == 0xFF808080

        surface.SDL_FreeSurface(imgsurf)


    @pytest.mark.skipif(not _HASNUMPY, reason="numpy module is not supported")
    def test_pixels2d(self):
        # Import test image and open pixels2d view
        imgsurf = surface.SDL_LoadBMP(self.testfile.encode("utf-8"))
        nparray = sdl2ext.pixels2d(imgsurf.contents, transpose=False)
        assert nparray.shape == (32, 32)

        # Test different coordinates on surface
        assert color.ARGB(nparray[0][0]) == colors['red']
        assert color.ARGB(nparray[0][16]) == colors['blue']
        assert color.ARGB(nparray[0][31]) == colors['white']
        assert color.ARGB(nparray[31][31]) == colors['black']

        # Try modifying surface, test if changes persist 
        nparray[31][0] = 0xFF808080 # medium grey in ARGB
        nparray2 = sdl2ext.pixels2d(imgsurf, transpose=False)
        assert nparray2[31][0] == 0xFF808080

        surface.SDL_FreeSurface(imgsurf)


    @pytest.mark.skipif(not _HASNUMPY, reason="numpy module is not supported")
    def test_pixels3d(self):
        # Import test image and convert to RGBA
        rgba = pixels.SDL_PIXELFORMAT_ABGR8888
        imgsurf = surface.SDL_LoadBMP(self.testfile.encode("utf-8"))
        imgsurf = surface.SDL_ConvertSurfaceFormat(imgsurf.contents, rgba, 0)

        # Create view and test different coordinates on surface
        nparray = sdl2ext.pixels3d(imgsurf.contents, transpose=False)
        assert nparray.shape == (32, 32, 4)
        assert color.Color(*nparray[0][0]) == colors['red']
        assert color.Color(*nparray[0][16]) == colors['blue']
        assert color.Color(*nparray[0][31]) == colors['white']
        assert color.Color(*nparray[31][31]) == colors['black']

        # Create transposed view and test different coordinates on surface
        nptrans = sdl2ext.pixels3d(imgsurf.contents, transpose=True)
        assert nptrans.shape == (32, 32, 4)
        assert color.Color(*nptrans[0][0]) == colors['red']
        assert color.Color(*nptrans[16][0]) == colors['blue']
        assert color.Color(*nptrans[31][0]) == colors['white']
        assert color.Color(*nptrans[31][31]) == colors['black']

        # Try modifying surface, test if changes persist 
        grey = [128, 128, 128, 255]
        nparray[31][0][:] = grey
        nparray2 = sdl2ext.pixels3d(imgsurf, transpose=False)
        assert color.Color(*nparray2[31][0]) == color.Color(*grey)

        surface.SDL_FreeSurface(imgsurf)


    @pytest.mark.skipif(not _HASNUMPY, reason="numpy module is not supported")
    def test_surface_to_ndarray(self):
        # Import test image & create an RGBA copy
        rgba = pixels.SDL_PIXELFORMAT_ABGR8888
        imgsurf = surface.SDL_LoadBMP(self.testfile.encode("utf-8"))
        rgbasurf = surface.SDL_ConvertSurfaceFormat(imgsurf.contents, rgba, 0)

        # Create a 2D ndarray from the surface & test different coordinates
        arr_2d = sdl2ext.surface_to_ndarray(imgsurf.contents, ndim=2)
        assert color.ARGB(arr_2d[0][0]) == colors['red']
        assert color.ARGB(arr_2d[0][16]) == colors['blue']
        assert color.ARGB(arr_2d[0][31]) == colors['white']
        assert color.ARGB(arr_2d[31][31]) == colors['black']

        # Create a 3D ndarray from the surface & test different coordinates
        arr_3d = sdl2ext.surface_to_ndarray(rgbasurf.contents)
        assert arr_3d.shape == (32, 32, 4)
        assert color.Color(*arr_3d[0][0]) == colors['red']
        assert color.Color(*arr_3d[0][16]) == colors['blue']
        assert color.Color(*arr_3d[0][31]) == colors['white']
        assert color.Color(*arr_3d[31][31]) == colors['black']

        # Try modifying surface, make sure changes don't persist
        grey = [128, 128, 128, 255]
        arr_3d[31][0][:] = grey
        arr_view = sdl2ext.pixels3d(rgbasurf, transpose=False)
        assert color.Color(*arr_view[31][0]) != color.Color(*grey)

        surface.SDL_FreeSurface(imgsurf)
