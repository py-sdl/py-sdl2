import os
import sys
import pytest
from sdl2 import ext as sdl2ext
from sdl2.ext import color
from sdl2 import surface
from sdl2 import pixels

try:
    from sdl2 import sdlimage
    _HASSDLIMAGE=True
except:
    _HASSDLIMAGE=False

try:
    import PIL
    _HASPIL = True
except ImportError:
    _HASPIL = False


parent_path = os.path.abspath(os.path.dirname(__file__))
resource_path = os.path.join(parent_path, "resources")

is32bit = sys.maxsize <= 2**32
ismacos = sys.platform == "darwin"
skip_formats = []

# SVG unsupported on SDL2_image < 2.0.2
if _HASSDLIMAGE and sdlimage.dll.version < 2002:
    skip_formats.append("svg")

# As of SDL2_image 2.0.5, XCF support seems to be broken on 32-bit builds
# XCF support is also broken in official SDL2_image macOS .frameworks
if is32bit or ismacos:
    skip_formats.append("xcf")

# WEBP support seems to be broken in the 32-bit Windows SDL2_image 2.0.2 binary
bad_webp = is32bit and sdlimage.dll.version == 2002
if bad_webp:
    skip_formats.remove("webp")


# List of lossy/non-color formats that shouldn't be compared against reference
# during tests
skip_color_check = ['gif', 'jpg', 'lbm', 'pbm', 'pgm', 'svg', 'webp']

colors = {
    'red': color.Color(255, 0, 0, 255),
    'blue': color.Color(0, 0, 255, 255),
    'black': color.Color(0, 0, 0, 255),
    'white': color.Color(255, 255, 255, 255)
}


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


    def check_image_contents(self, img):
        # Test different coordinates on surface
        pxview = sdl2ext.PixelView(img)
        match = (
            color.ARGB(pxview[0][0]) == colors['red'] and
            color.ARGB(pxview[0][16]) == colors['blue'] and
            color.ARGB(pxview[0][31]) == colors['white'] and
            color.ARGB(pxview[31][31]) == colors['black']
        )
        del pxview
        return match


    def test_load_bmp(self):
        # Test loading a basic BMP image
        img_path = os.path.join(resource_path, "surfacetest.bmp")
        sf = sdl2ext.load_bmp(img_path)
        assert isinstance(sf, surface.SDL_Surface)
        assert self.check_image_contents(sf)
        surface.SDL_FreeSurface(sf)

        # Test exception on missing file
        bad_path = os.path.join(resource_path, "doesnt_exist.bmp")
        with pytest.raises(IOError):
            sdl2ext.load_bmp(bad_path)

        # Test exception on bad file type
        bad_type = os.path.join(resource_path, "surfacetest.png")
        with pytest.raises(sdl2ext.SDLError):
            sdl2ext.load_bmp(bad_type)


    def test_save_bmp(self, tmpdir):
        # Open a BMP that we can re-save
        img_path = os.path.join(resource_path, "surfacetest.bmp")
        sf = sdl2ext.load_bmp(img_path)
        assert isinstance(sf, surface.SDL_Surface)

        # Try saving the BMP to a new folder and re-loading it
        outpath = os.path.join(str(tmpdir), "save_test.bmp")
        sdl2ext.save_bmp(sf, outpath)
        assert os.path.exists(outpath)
        sf_saved = sdl2ext.load_bmp(outpath)
        assert isinstance(sf_saved, surface.SDL_Surface)
        assert self.check_image_contents(sf_saved)

        # Try modifying/overwriting the existing BMP
        sdl2ext.fill(sf, (0, 255, 0, 255))
        sdl2ext.save_bmp(sf, outpath, overwrite=True)
        sf_saved2 = sdl2ext.load_bmp(outpath)
        assert isinstance(sf_saved2, surface.SDL_Surface)
        assert not self.check_image_contents(sf_saved2)

        # Test existing file exception with overwrite=False
        with pytest.raises(RuntimeError):
            sdl2ext.save_bmp(sf_saved, outpath, overwrite=False)
        
        # Test exception with non-existent save directory
        bad_path = os.path.join(resource_path, "doesnt_exist", "tst.bmp")
        with pytest.raises(IOError):
            sdl2ext.save_bmp(sf_saved, bad_path)


    def test_load_img(self):
        # Test loading all test images, with and without ARGB conversion
        resources = os.listdir(resource_path)
        test_imgs = [f for f in resources if f[:11] == "surfacetest"]
        for img in test_imgs:
            img_path = os.path.join(resource_path, img)
            fmt = img.split(".")[-1]
            if fmt in skip_formats:
                continue

            sf = sdl2ext.load_img(img_path)
            assert isinstance(sf, surface.SDL_Surface)
            assert sf.format.contents.format == pixels.SDL_PIXELFORMAT_ARGB8888
            if fmt not in skip_color_check:
                assert self.check_image_contents(sf)
            surface.SDL_FreeSurface(sf)

            sf2 = sdl2ext.load_img(img_path, as_argb=False)
            assert isinstance(sf2, surface.SDL_Surface)
            surface.SDL_FreeSurface(sf2)

        # Test exception on missing file
        bad_path = os.path.join(resource_path, "doesnt_exist.bmp")
        with pytest.raises(IOError):
            sdl2ext.load_img(bad_path)

        # Test exception on bad file type
        bad_type = os.path.join(resource_path, "tuffy.ttf")
        with pytest.raises(sdl2ext.SDLError):
            sdl2ext.load_img(bad_type)


    @pytest.mark.skipif(not _HASPIL, reason="Pillow library is not installed")
    def test_pillow_to_image(self):
        # Import an image using Pillow
        from PIL import Image
        img_path = os.path.join(resource_path, "surfacetest.bmp")
        pil_img = Image.open(img_path)

        # Convert the image to an SDL surface and verify it worked
        sf = sdl2ext.pillow_to_surface(pil_img)
        assert isinstance(sf, surface.SDL_Surface)
        assert self.check_image_contents(sf)
        surface.SDL_FreeSurface(sf)

        # Try converting a palette image
        palette_img = pil_img.convert("P", palette=Image.WEB)
        sfp = sdl2ext.pillow_to_surface(palette_img)
        pxformat = sfp.format.contents
        assert isinstance(sfp, surface.SDL_Surface)
        assert self.check_image_contents(sfp)
        assert pxformat.BytesPerPixel == 4
        surface.SDL_FreeSurface(sfp)

        # Try converting a palette image without ARGB conversion
        sfp2 = sdl2ext.pillow_to_surface(palette_img, False)
        pxformat = sfp2.format.contents
        assert isinstance(sfp2, surface.SDL_Surface)
        assert pxformat.BytesPerPixel == 1
        sdl_palette = pxformat.palette.contents
        pil_palette = palette_img.getpalette()
        assert sdl_palette.colors[0].r == pil_palette[0]
        assert sdl_palette.colors[0].g == pil_palette[1]
        assert sdl_palette.colors[0].b == pil_palette[2]
        surface.SDL_FreeSurface(sfp2)

        # Test loading all supported test images and compare against reference
        resources = os.listdir(resource_path)
        test_imgs = [f for f in resources if f[:11] == "surfacetest"]
        for img in test_imgs:
            fmt = img.split(".")[-1]
            if fmt in ("webp", "xcf", "lbm", "svg"):
                continue
            pil_img = Image.open(os.path.join(resource_path, img))
            sf = sdl2ext.pillow_to_surface(pil_img)
            assert isinstance(sf, surface.SDL_Surface)
            assert sf.format.contents.format == pixels.SDL_PIXELFORMAT_ARGB8888
            if fmt not in skip_color_check:
                assert self.check_image_contents(sf)
            surface.SDL_FreeSurface(sf)


    def test_load_image(self):
        resources = os.listdir(resource_path)
        test_imgs = [f for f in resources if f[:11] == "surfacetest"]
        for img in test_imgs:
            img_path = os.path.join(resource_path, img)
            fmt = img.split(".")[-1]
            if fmt in skip_formats:
                continue

            # Try normal loading
            sf = sdl2ext.load_image(img_path)
            assert isinstance(sf, surface.SDL_Surface)

            # Force only PIL
            if _HASPIL and fmt not in ("webp", "xcf", "lbm", "svg"):
                sf = sdl2ext.load_image(img_path, enforce="PIL")
                assert isinstance(sf, surface.SDL_Surface)

            # Force only sdlimage
            sf = sdl2ext.load_image(img_path, enforce="SDL")
            assert isinstance(sf, surface.SDL_Surface)
