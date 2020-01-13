import os
import sys
import pytest
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_VIDEO
from sdl2 import surface

sdlgfx = pytest.importorskip("sdl2.sdlgfx")


class TestSDLGFX(object):
    __tags__ = ["sdl", "sdlgfx"]

    @classmethod
    def setup_class(cls):
        if SDL_Init(SDL_INIT_VIDEO) != 0:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    @pytest.mark.skip("not implemented")
    def test_FPSManager(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_initFramerate(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_getFramerate(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_setFramerate(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_getFramecount(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_framerateDelay(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_pixelColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_pixelRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_hlineColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_hlineRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_vlineColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_vlineRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_rectangleColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_rectangleRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_roundedRectangleColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_roundedRectangleRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_boxColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_boxRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_roundedBoxColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_roundedBoxRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_lineColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_lineRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_aalineColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_aalineRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_thickLineColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_thickLineRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_circleColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_circleRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_arcColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_arcRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_aacircleColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_aacircleRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_filledCircleColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_filledCircleRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_ellipseColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_ellipseRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_aaellipseColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_aaellipseRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_filledEllipseColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_filledEllipseRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_pieColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_pieRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_filledPieColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_filledPieRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_trigonColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_trigonRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_aatrigonColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_aatrigonRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_filledTrigonColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_filledTrigonRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_polygonColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_polygonRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_aapolygonColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_aapolygonRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_filledPolygonColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_filledPolygonRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_texturedPolygon(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_bezierColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_bezierRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_gfxPrimitivesSetFont(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_gfxPrimitivesSetFontRotation(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_characterColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_characterRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_stringColor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_stringRGBA(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_rotozoomSurface(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_rotozoomSurfaceXY(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_rotozoomSurfaceSize(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_rotozoomSurfaceSizeXY(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_zoomSurface(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_zoomSurfaceSize(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_shrinkSurface(self):
        pass

    def test_rotateSurface90Degrees(self):
        w, h = 470, 530
        sf = surface.SDL_CreateRGBSurface(0, w, h, 32, 0, 0, 0, 0)
        assert isinstance(sf.contents, surface.SDL_Surface)

        rotsf = sdlgfx.rotateSurface90Degrees(sf, 1)
        assert isinstance(rotsf.contents, surface.SDL_Surface)
        assert rotsf.contents.w == h
        assert rotsf.contents.h == w

        surface.SDL_FreeSurface(rotsf)
        surface.SDL_FreeSurface(sf)
