import os
import sys
import ctypes
import pytest
from sdl2 import SDL_Init, SDL_Quit, version, surface, rwops, render

sdlimage = pytest.importorskip("sdl2.sdlimage")


is32bit = sys.maxsize <= 2**32
ismacos = sys.platform == "darwin"

formats = ["bmp",
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
           #"xv",
           ]

# SVG unsupported on SDL2_image < 2.0.2
if sdlimage.dll.version < 2002:
    formats.remove("svg")

# As of SDL2_image 2.0.5, XCF support seems to be broken on 32-bit builds
# XCF support is also broken in official SDL2_image macOS .frameworks
if is32bit or ismacos:
    formats.remove("xcf")


def test_IMG_Linked_Version():
    v = sdlimage.IMG_Linked_Version()
    assert isinstance(v.contents, version.SDL_version)
    assert v.contents.major == 2
    assert v.contents.minor == 0
    assert v.contents.patch >= 1

def test_IMG_Init():
    SDL_Init(0)
    libs = {
        'JPEG': sdlimage.IMG_INIT_JPG,
        'PNG': sdlimage.IMG_INIT_PNG,
        'TIFF': sdlimage.IMG_INIT_TIF,
        'WEBP': sdlimage.IMG_INIT_WEBP
    }
    for lib in libs.keys():
        flags = libs[lib]
        ret = sdlimage.IMG_Init(flags)
        err = sdlimage.IMG_GetError()
        assert ret & flags == flags
        sdlimage.IMG_Quit()
    SDL_Quit()


class TestSDLImage(object):
    __tags__ = ["sdl", "sdlimage"]

    @classmethod
    def setup_class(cls):
        flags = (
            sdlimage.IMG_INIT_JPG | sdlimage.IMG_INIT_PNG |
            sdlimage.IMG_INIT_TIF  | sdlimage.IMG_INIT_WEBP
        )
        SDL_Init(0)
        sdlimage.IMG_Init(flags)

    @classmethod
    def teardown_class(cls):
        sdlimage.IMG_Quit()
        SDL_Quit()

    def test_IMG_Load(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            sf = sdlimage.IMG_Load(filename.encode("utf-8"))
            assert isinstance(sf.contents, surface.SDL_Surface)
            surface.SDL_FreeSurface(sf)

    def test_IMG_Load_RW(self):
        skip = ['tga'] # TGA broken for Load_RW
        fname = "surfacetest.%s"
        for fmt in formats:
            if fmt in skip:
                continue
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                sf = sdlimage.IMG_Load_RW(rwops.rw_from_object(fp), False)
            assert isinstance(sf.contents, surface.SDL_Surface)
            surface.SDL_FreeSurface(sf)

    def test_IMG_LoadTexture(self):
        sf = surface.SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        rd = render.SDL_CreateSoftwareRenderer(sf)
        skip = []
        fname = "surfacetest.%s"
        for fmt in formats:
            if fmt in skip:
                continue
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            tex = sdlimage.IMG_LoadTexture(rd, filename.encode("utf-8"))
            assert isinstance(tex.contents, render.SDL_Texture)
            render.SDL_DestroyTexture(tex)

        #self.assertRaises(sdl.SDLError, sdlimage.load_texture, rd,
        #                  RESOURCES.get_path("rwopstest.txt"))

        #self.assertRaises(sdl.SDLError, sdlimage.load_texture, rd, None)
        #self.assertRaises(sdl.SDLError, sdlimage.load_texture, rd, 1234)
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlimage.load_texture, None,
        #                  RESOURCES.get_path("surfacetest.bmp"))
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlimage.load_texture, "Test",
        #                  RESOURCES.get_path("surfacetest.bmp"))
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlimage.load_texture, 1234,
        #                  RESOURCES.get_path("surfacetest.bmp"))

        render.SDL_DestroyRenderer(rd)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadTexture_RW(self):
        sf = surface.SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        rd = render.SDL_CreateSoftwareRenderer(sf)
        skip = ['svg', 'tga'] # TGA & SVG broken for LoadTexture_RW
        fname = "surfacetest.%s"
        for fmt in formats:
            if fmt in skip:
                continue
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                tex = sdlimage.IMG_LoadTexture_RW(rd, rwops.rw_from_object(fp), 0)
                assert tex is not None
                assert isinstance(tex.contents, render.SDL_Texture)
                render.SDL_DestroyTexture(tex)

        render.SDL_DestroyRenderer(rd)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadTextureTyped_RW(self):
        sf = surface.SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        rd = render.SDL_CreateSoftwareRenderer(sf)
        skip = ['svg'] # SVG broken for LoadTextureTyped_RW
        fname = "surfacetest.%s"
        for fmt in formats:
            if fmt in skip:
                continue
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                rw = rwops.rw_from_object(fp)
                fmtx = fmt.upper().encode("utf-8")
                tex = sdlimage.IMG_LoadTextureTyped_RW(rd, rw, 0, fmtx)
                assert tex is not None
                assert isinstance(tex.contents, render.SDL_Texture)
            render.SDL_DestroyTexture(tex)
        render.SDL_DestroyRenderer(rd)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadTyped_RW(self):
        skip = []
        fname = "surfacetest.%s"
        for fmt in formats:
            if fmt in skip:
                continue
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                sf = sdlimage.IMG_LoadTyped_RW(rwops.rw_from_object(fp), False,
                                            fmt.upper().encode("utf-8"))
                assert isinstance(sf.contents, surface.SDL_Surface)
                surface.SDL_FreeSurface(sf)

    def test_IMG_LoadBMP_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.bmp"), "rb")
        sf = sdlimage.IMG_LoadBMP_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadCUR_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.cur"), "rb")
        sf = sdlimage.IMG_LoadCUR_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadGIF_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.gif"), "rb")
        sf = sdlimage.IMG_LoadGIF_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadICO_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.ico"), "rb")
        sf = sdlimage.IMG_LoadICO_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadJPG_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.jpg"), "rb")
        sf = sdlimage.IMG_LoadJPG_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadLBM_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.lbm"), "rb")
        sf = sdlimage.IMG_LoadLBM_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadPCX_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.pcx"), "rb")
        sf = sdlimage.IMG_LoadPCX_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadPNG_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.png"), "rb")
        sf = sdlimage.IMG_LoadPNG_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadPNM_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.pnm"), "rb")
        sf = sdlimage.IMG_LoadPNM_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    @pytest.mark.skipif(sdlimage.dll.version < 2002, reason="Added in 2.0.2")
    def test_IMG_LoadSVG_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.svg"), "rb")
        sf = sdlimage.IMG_LoadSVG_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadTGA_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.tga"), "rb")
        sf = sdlimage.IMG_LoadTGA_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadTIF_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.tif"), "rb")
        sf = sdlimage.IMG_LoadTIF_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadWEBP_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.webp"), "rb")
        sf = sdlimage.IMG_LoadWEBP_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    @pytest.mark.xfail(is32bit or ismacos, reason="XCF currently broken on 32-bit and macOS")
    def test_IMG_LoadXCF_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.xcf"), "rb")
        sf = sdlimage.IMG_LoadXCF_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_LoadXPM_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.xpm"), "rb")
        sf = sdlimage.IMG_LoadXPM_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    @pytest.mark.skip("not implemented")
    def test_IMG_LoadXV_RW(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.xv"), "rb")
        sf = sdlimage.IMG_LoadXV_RW(rwops.rw_from_object(fp))
        fp.close()
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    def test_IMG_isBMP(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "bmp":
                    assert sdlimage.IMG_isBMP(imgrw)
                else:
                    assert not sdlimage.IMG_isBMP(imgrw)

    def test_IMG_isCUR(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "cur":
                    assert sdlimage.IMG_isCUR(imgrw)
                else:
                    assert not sdlimage.IMG_isCUR(imgrw)

    def test_IMG_isGIF(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "gif":
                    assert sdlimage.IMG_isGIF(imgrw)
                else:
                    assert not sdlimage.IMG_isGIF(imgrw)

    def test_IMG_isICO(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "ico":
                    assert sdlimage.IMG_isICO(imgrw)
                else:
                    assert not sdlimage.IMG_isICO(imgrw)

    def test_IMG_isJPG(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "jpg":
                    assert sdlimage.IMG_isJPG(imgrw)
                else:
                    assert not sdlimage.IMG_isJPG(imgrw)

    def test_IMG_isLBM(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "lbm":
                    assert sdlimage.IMG_isLBM(imgrw)
                else:
                    assert not sdlimage.IMG_isLBM(imgrw)

    def test_IMG_isPCX(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "pcx":
                    assert sdlimage.IMG_isPCX(imgrw)
                else:
                    assert not sdlimage.IMG_isPCX(imgrw)

    def test_IMG_isPNG(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "png":
                    assert sdlimage.IMG_isPNG(imgrw)
                else:
                    assert not sdlimage.IMG_isPNG(imgrw)

    def test_IMG_isPNM(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt in ("pnm", "pbm", "ppm", "pgm"):
                    assert sdlimage.IMG_isPNM(imgrw)
                else:
                    assert not sdlimage.IMG_isPNM(imgrw)

    @pytest.mark.skipif(sdlimage.dll.version < 2002, reason="Added in 2.0.2")
    def test_IMG_isSVG(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "svg":
                    assert sdlimage.IMG_isSVG(imgrw)
                else:
                    assert not sdlimage.IMG_isSVG(imgrw)

    def test_IMG_isTIF(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "tif":
                    assert sdlimage.IMG_isTIF(imgrw)
                else:
                    assert not sdlimage.IMG_isTIF(imgrw)

    def test_IMG_isWEBP(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "webp":
                    assert sdlimage.IMG_isWEBP(imgrw)
                else:
                    assert not sdlimage.IMG_isWEBP(imgrw)

    @pytest.mark.xfail(ismacos, reason="XCF currently broken on macOS")
    def test_IMG_isXCF(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "xcf":
                    assert sdlimage.IMG_isXCF(imgrw)
                else:
                    assert not sdlimage.IMG_isXCF(imgrw)

    def test_IMG_isXPM(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "xpm":
                    assert sdlimage.IMG_isXPM(imgrw)
                else:
                    assert not sdlimage.IMG_isXPM(imgrw)

    @pytest.mark.skip("not implemented")
    def test_IMG_isXV(self):
        fname = "surfacetest.%s"
        for fmt in formats:
            testdir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(testdir, "resources", fname % fmt)
            with open(filename, "rb") as fp:
                imgrw = rwops.rw_from_object(fp)
                if fmt == "xv":
                    assert sdlimage.IMG_isXV(imgrw)
                else:
                    assert not sdlimage.IMG_isXV(imgrw)

    @pytest.mark.skipif(hasattr(sys, "pypy_version_info"),
        reason="PyPy's ctypes fails to pass a correct string array")
    def test_IMG_ReadXPMFromArray(self):
        testdir = os.path.dirname(os.path.abspath(__file__))
        fp = open(os.path.join(testdir, "resources", "surfacetest.xpm"), "rb")
        xpm = b""
        fp.readline()  # /* XPM */
        fp.readline()  # static char * surfacetest_xpm[] = {
        lbuf = fp.readlines()
        fp.close()
        for line in lbuf:
            if line.endswith(b"};"):
                xpm += line[1:-4]
            else:
                xpm += line[1:-3]
        pxpm = ctypes.c_char_p(xpm)
        sf = sdlimage.IMG_ReadXPMFromArray(ctypes.byref(pxpm))
        assert isinstance(sf.contents, surface.SDL_Surface)
        surface.SDL_FreeSurface(sf)

    @pytest.mark.skip("not implemented")
    def test_IMG_SavePNG(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_IMG_SavePNG_RW(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_IMG_SaveJPG(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_IMG_SaveJPG_RW(self):
        pass
