import sys
import unittest
from .. import ext as sdl2ext
from .. import surface

RESOURCES = sdl2ext.Resources(__file__, "resources")

formats = [  # Do not use bmp - it's contained in resources.zip
           "cur",
           "gif",
           "ico",
           "jpg",
           "lbm",
           "pbm",
           "pcx",
           "pgm",
           "png",
           "pnm",
           "ppm",
           "tga",
           "tif",
           "webp",
           "xcf",
           "xpm",
           # "xv",
           ]


class SDL2ExtImageTest(unittest.TestCase):
    __tags__ = ["sdl", "sdl2ext"]

    def setUp(self):
        sdl2ext.init()

    def tearDown(self):
        sdl2ext.quit()

    def test_get_image_formats(self):
        self.assertIsInstance(sdl2ext.get_image_formats(), tuple)
        supformats = sdl2ext.get_image_formats()
        for fmt in formats:
            self.assertTrue(fmt in supformats)

    def test_load_image(self):
        # TODO: add image comparision to check, if it actually does the
        # right thing (SDL2 BMP loaded image?)
        # Add argument tests
        try:
            import PIL
            _HASPIL = True
        except ImportError:
            _HASPIL = False

        fname = "surfacetest.%s"
        for fmt in formats:
            filename = RESOURCES.get_path(fname % fmt)
            sf = sdl2ext.load_image(filename)
            self.assertIsInstance(sf, surface.SDL_Surface)

            # Force only PIL
            if _HASPIL and fmt not in ("webp", "xcf", "lbm"):
                sf = sdl2ext.load_image(filename, enforce="PIL")
                self.assertIsInstance(sf, surface.SDL_Surface)

            # Force only mule.sdlimage
            sf = sdl2ext.load_image(filename, enforce="SDL")
            self.assertIsInstance(sf, surface.SDL_Surface)


if __name__ == '__main__':
    sys.exit(unittest.main())
