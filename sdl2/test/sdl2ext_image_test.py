import sys
import pytest
from sdl2 import ext as sdl2ext
from sdl2 import surface

try:
    from sdl2 import sdlimage
    _HASSDLIMAGE=True
except:
    _HASSDLIMAGE=False

RESOURCES = sdl2ext.Resources(__file__, "resources")

is32bit = sys.maxsize <= 2**32
ismacos = sys.platform == "darwin"

formats = [ # Do not use bmp - it's contained in resources.zip
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
           "svg",
           "tga",
           "tif",
           "webp",
           "xcf",
           "xpm",
           # "xv",
           ]

# SVG unsupported on SDL2_image < 2.0.2
if _HASSDLIMAGE and sdlimage.dll.version < 2002:
    formats.remove("svg")

# As of SDL2_image 2.0.5, XCF support seems to be broken on 32-bit builds
# XCF support is also broken in official SDL2_image macOS .frameworks
if is32bit or ismacos:
    formats.remove("xcf")


class TestSDL2ExtImage(object):
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

    def test_get_image_formats(self):
        assert isinstance(sdl2ext.get_image_formats(), tuple)
        supformats = sdl2ext.get_image_formats()
        for fmt in formats:
            assert fmt in supformats

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
            assert isinstance(sf, surface.SDL_Surface)

            # Force only PIL
            if _HASPIL and fmt not in ("webp", "xcf", "lbm", "svg"):
                sf = sdl2ext.load_image(filename, enforce="PIL")
                assert isinstance(sf, surface.SDL_Surface)

            # Force only sdlimage
            sf = sdl2ext.load_image(filename, enforce="SDL")
            assert isinstance(sf, surface.SDL_Surface)
