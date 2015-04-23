import os
import sys
import unittest
from .. import SDL_Init, SDL_Quit, SDL_INIT_VIDEO
from .. import surface, sdlgfx

class SDLTTFTest(unittest.TestCase):
    __tags__ = ["sdl", "sdlgfx"]

    def setUp(self):
        SDL_Init(SDL_INIT_VIDEO)

    def tearDown(self):
        SDL_Quit()

    @unittest.skip("not implemented")
    def test_FPSManager(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_initFramerate(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_getFramerate(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_setFramerate(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_getFramecount(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_framerateDelay(self):
        pass

    @unittest.skip("not implemented")
    def test_pixelColor(self):
        pass

    @unittest.skip("not implemented")
    def test_pixelRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_hlineColor(self):
        pass

    @unittest.skip("not implemented")
    def test_hlineRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_vlineColor(self):
        pass

    @unittest.skip("not implemented")
    def test_vlineRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_rectangleColor(self):
        pass

    @unittest.skip("not implemented")
    def test_rectangleRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_roundedRectangleColor(self):
        pass

    @unittest.skip("not implemented")
    def test_roundedRectangleRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_boxColor(self):
        pass

    @unittest.skip("not implemented")
    def test_boxRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_roundedBoxColor(self):
        pass

    @unittest.skip("not implemented")
    def test_roundedBoxRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_lineColor(self):
        pass

    @unittest.skip("not implemented")
    def test_lineRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_aalineColor(self):
        pass

    @unittest.skip("not implemented")
    def test_aalineRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_thickLineColor(self):
        pass

    @unittest.skip("not implemented")
    def test_thickLineRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_circleColor(self):
        pass

    @unittest.skip("not implemented")
    def test_circleRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_arcColor(self):
        pass

    @unittest.skip("not implemented")
    def test_arcRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_aacircleColor(self):
        pass

    @unittest.skip("not implemented")
    def test_aacircleRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_filledCircleColor(self):
        pass

    @unittest.skip("not implemented")
    def test_filledCircleRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_ellipseColor(self):
        pass

    @unittest.skip("not implemented")
    def test_ellipseRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_aaellipseColor(self):
        pass

    @unittest.skip("not implemented")
    def test_aaellipseRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_filledEllipseColor(self):
        pass

    @unittest.skip("not implemented")
    def test_filledEllipseRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_pieColor(self):
        pass

    @unittest.skip("not implemented")
    def test_pieRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_filledPieColor(self):
        pass

    @unittest.skip("not implemented")
    def test_filledPieRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_trigonColor(self):
        pass

    @unittest.skip("not implemented")
    def test_trigonRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_aatrigonColor(self):
        pass

    @unittest.skip("not implemented")
    def test_aatrigonRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_filledTrigonColor(self):
        pass

    @unittest.skip("not implemented")
    def test_filledTrigonRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_polygonColor(self):
        pass

    @unittest.skip("not implemented")
    def test_polygonRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_aapolygonColor(self):
        pass

    @unittest.skip("not implemented")
    def test_aapolygonRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_filledPolygonColor(self):
        pass

    @unittest.skip("not implemented")
    def test_filledPolygonRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_texturedPolygon(self):
        pass

    @unittest.skip("not implemented")
    def test_bezierColor(self):
        pass

    @unittest.skip("not implemented")
    def test_bezierRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_gfxPrimitivesSetFont(self):
        pass

    @unittest.skip("not implemented")
    def test_gfxPrimitivesSetFontRotation(self):
        pass

    @unittest.skip("not implemented")
    def test_characterColor(self):
        pass

    @unittest.skip("not implemented")
    def test_characterRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_stringColor(self):
        pass

    @unittest.skip("not implemented")
    def test_stringRGBA(self):
        pass

    @unittest.skip("not implemented")
    def test_rotozoomSurface(self):
        pass

    @unittest.skip("not implemented")
    def test_rotozoomSurfaceXY(self):
        pass

    @unittest.skip("not implemented")
    def test_rotozoomSurfaceSize(self):
        pass

    @unittest.skip("not implemented")
    def test_rotozoomSurfaceSizeXY(self):
        pass

    @unittest.skip("not implemented")
    def test_zoomSurface(self):
        pass

    @unittest.skip("not implemented")
    def test_zoomSurfaceSize(self):
        pass

    @unittest.skip("not implemented")
    def test_shrinkSurface(self):
        pass

    def test_rotateSurface90Degrees(self):
        w, h = 470, 530
        sf = surface.SDL_CreateRGBSurface(0, w, h, 32, 0, 0, 0, 0)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)

        rotsf = sdlgfx.rotateSurface90Degrees(sf, 1)
        self.assertIsInstance(rotsf.contents, surface.SDL_Surface)
        self.assertEqual(rotsf.contents.w, h)
        self.assertEqual(rotsf.contents.h, w)

        surface.SDL_FreeSurface(rotsf)
        surface.SDL_FreeSurface(sf)


if __name__ == '__main__':
    sys.exit(unittest.main())
