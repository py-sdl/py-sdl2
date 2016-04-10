import sys
import unittest
import copy
from ctypes import c_int, POINTER, byref, cast, ArgumentError
from .. import SDL_Init, SDL_Quit, SDL_QuitSubSystem, SDL_INIT_EVERYTHING
from .. import pixels
from ..pixels import SDL_Color
from ..stdinc import Uint8, Uint16, Uint32


class SDLPixelsTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(SDL_INIT_EVERYTHING)

    def tearDown(self):
        SDL_QuitSubSystem(SDL_INIT_EVERYTHING)
        SDL_Quit()

    def test_SDL_FOURCC(self):
        self.assertRaises(TypeError, pixels.SDL_FOURCC, None, None, None, None)
        self.assertRaises(TypeError, pixels.SDL_FOURCC, "a", None, None, None)
        self.assertRaises(TypeError, pixels.SDL_FOURCC, None, "a", None, None)
        self.assertRaises(TypeError, pixels.SDL_FOURCC, None, None, "a", None)
        self.assertRaises(TypeError, pixels.SDL_FOURCC, None, None, None, "a")
        self.assertRaises(TypeError, pixels.SDL_FOURCC, "a", "a", None, None)
        self.assertRaises(TypeError, pixels.SDL_FOURCC, "a", "a", "a", None)
        self.assertRaises(TypeError, pixels.SDL_FOURCC, "a", "a", "a", 1)
        self.assertRaises(TypeError, pixels.SDL_FOURCC, "a", "a", 5, 1)
        self.assertRaises(TypeError, pixels.SDL_FOURCC, "a", 17, 5, 1)
        self.assertEqual(pixels.SDL_FOURCC("0", "0", "0", "0"), 0x30303030)
        self.assertEqual(pixels.SDL_FOURCC("1", "1", "1", "1"), 0x31313131)
        self.assertEqual(pixels.SDL_FOURCC("1", "2", "3", "4"), 0x34333231)
        self.assertEqual(pixels.SDL_FOURCC("4", "3", "2", "1"), 0x31323334)

    def test_SDL_DEFINE_PIXELFORMAT(self):
        fmt = pixels.SDL_DEFINE_PIXELFORMAT(pixels.SDL_PIXELTYPE_INDEX1,
                                            pixels.SDL_BITMAPORDER_4321, 0,
                                            1, 0)
        self.assertEqual(fmt, pixels.SDL_PIXELFORMAT_INDEX1LSB)

        fmt = pixels.SDL_DEFINE_PIXELFORMAT(pixels.SDL_PIXELTYPE_PACKED16,
                                            pixels.SDL_PACKEDORDER_XRGB,
                                            pixels.SDL_PACKEDLAYOUT_4444,
                                            12, 2)
        self.assertEqual(fmt, pixels.SDL_PIXELFORMAT_RGB444)

        fmt = pixels.SDL_DEFINE_PIXELFORMAT(pixels.SDL_PIXELTYPE_PACKED16,
                                            pixels.SDL_PACKEDORDER_ABGR,
                                            pixels.SDL_PACKEDLAYOUT_1555,
                                            16, 2)
        self.assertEqual(fmt, pixels.SDL_PIXELFORMAT_ABGR1555)

    def test_SDL_PIXELTYPE(self):
        pixtype = pixels.SDL_PIXELTYPE
        self.assertEqual(pixtype(pixels.SDL_PIXELFORMAT_INDEX1LSB),
                         pixels.SDL_PIXELTYPE_INDEX1)
        self.assertEqual(pixtype(pixels.SDL_PIXELFORMAT_INDEX1MSB),
                         pixels.SDL_PIXELTYPE_INDEX1)
        self.assertEqual(pixtype(pixels.SDL_PIXELFORMAT_INDEX4LSB),
                         pixels.SDL_PIXELTYPE_INDEX4)
        self.assertEqual(pixtype(pixels.SDL_PIXELFORMAT_ARGB8888),
                         pixels.SDL_PIXELTYPE_PACKED32)

    def test_SDL_PIXELORDER(self):
        pixorder = pixels.SDL_PIXELORDER
        self.assertEqual(pixorder(pixels.SDL_PIXELFORMAT_INDEX1LSB),
                         pixels.SDL_BITMAPORDER_4321)
        self.assertEqual(pixorder(pixels.SDL_PIXELFORMAT_INDEX1MSB),
                         pixels.SDL_BITMAPORDER_1234)
        self.assertEqual(pixorder(pixels.SDL_PIXELFORMAT_INDEX4LSB),
                         pixels.SDL_BITMAPORDER_4321)
        self.assertEqual(pixorder(pixels.SDL_PIXELFORMAT_ARGB8888),
                         pixels.SDL_PACKEDORDER_ARGB)

    def test_SDL_PIXELLAYOUT(self):
        pixlayout = pixels.SDL_PIXELLAYOUT
        self.assertEqual(pixlayout(pixels.SDL_PIXELFORMAT_INDEX1LSB),
                         pixels.SDL_PACKEDLAYOUT_NONE)
        self.assertEqual(pixlayout(pixels.SDL_PIXELFORMAT_RGB332),
                         pixels.SDL_PACKEDLAYOUT_332)
        self.assertEqual(pixlayout(pixels.SDL_PIXELFORMAT_ARGB8888),
                         pixels.SDL_PACKEDLAYOUT_8888)

    def test_SDL_BITSPERPIXEL(self):
        bitspp = pixels.SDL_BITSPERPIXEL
        self.assertEqual(bitspp(pixels.SDL_PIXELFORMAT_INDEX1LSB), 1)
        self.assertEqual(bitspp(pixels.SDL_PIXELFORMAT_INDEX4LSB), 4)
        self.assertEqual(bitspp(pixels.SDL_PIXELFORMAT_RGB332), 8)
        self.assertEqual(bitspp(pixels.SDL_PIXELFORMAT_ARGB8888), 32)
        # TODO: clarify
        # self.assertEqual(bitspp(pixels.SDL_PIXELFORMAT_YUY2), 85)
        # self.assertEqual(bitspp(pixels.SDL_PIXELFORMAT_IYUV), 89)
        # self.assertEqual(bitspp(pixels.SDL_PIXELFORMAT_UYVY), 89)

    def test_SDL_BYTESPERPIXEL(self):
        bytespp = pixels.SDL_BYTESPERPIXEL
        self.assertEqual(bytespp(pixels.SDL_PIXELFORMAT_INDEX1LSB), 0)
        self.assertEqual(bytespp(pixels.SDL_PIXELFORMAT_INDEX4LSB), 0)
        self.assertEqual(bytespp(pixels.SDL_PIXELFORMAT_RGB332), 1)
        self.assertEqual(bytespp(pixels.SDL_PIXELFORMAT_ARGB8888), 4)
        self.assertEqual(bytespp(pixels.SDL_PIXELFORMAT_YUY2), 2)
        self.assertEqual(bytespp(pixels.SDL_PIXELFORMAT_IYUV), 1)
        self.assertEqual(bytespp(pixels.SDL_PIXELFORMAT_UYVY), 2)

    def test_SDL_ISPIXELFORMAT_INDEXED(self):
        isindexed = pixels.SDL_ISPIXELFORMAT_INDEXED
        self.assertTrue(isindexed(pixels.SDL_PIXELFORMAT_INDEX1LSB))
        self.assertTrue(isindexed(pixels.SDL_PIXELFORMAT_INDEX1MSB))
        self.assertTrue(isindexed(pixels.SDL_PIXELFORMAT_INDEX4LSB))
        self.assertTrue(isindexed(pixels.SDL_PIXELFORMAT_INDEX4MSB))
        self.assertTrue(isindexed(pixels.SDL_PIXELFORMAT_INDEX8))
        self.assertFalse(isindexed(pixels.SDL_PIXELFORMAT_RGB332))
        self.assertFalse(isindexed(pixels.SDL_PIXELFORMAT_ARGB8888))
        self.assertFalse(isindexed(pixels.SDL_PIXELFORMAT_YUY2))

    def test_SDL_ISPIXELFORMAT_ALPHA(self):
        isalpha = pixels.SDL_ISPIXELFORMAT_ALPHA
        self.assertTrue(isalpha(pixels.SDL_PIXELFORMAT_ARGB8888))
        self.assertTrue(isalpha(pixels.SDL_PIXELFORMAT_RGBA8888))
        self.assertTrue(isalpha(pixels.SDL_PIXELFORMAT_RGBA4444))
        self.assertTrue(isalpha(pixels.SDL_PIXELFORMAT_ABGR1555))
        self.assertFalse(isalpha(pixels.SDL_PIXELFORMAT_INDEX1LSB))
        self.assertFalse(isalpha(pixels.SDL_PIXELFORMAT_INDEX4MSB))
        self.assertFalse(isalpha(pixels.SDL_PIXELFORMAT_RGB332))
        self.assertFalse(isalpha(pixels.SDL_PIXELFORMAT_YUY2))
        self.assertFalse(isalpha(pixels.SDL_PIXELFORMAT_RGBX8888))

    def test_SDL_ISPIXELFORMAT_FOURCC(self):
        isfourcc = pixels.SDL_ISPIXELFORMAT_FOURCC
        self.assertTrue(isfourcc(pixels.SDL_PIXELFORMAT_YV12))
        self.assertTrue(isfourcc(pixels.SDL_PIXELFORMAT_IYUV))
        self.assertTrue(isfourcc(pixels.SDL_PIXELFORMAT_YUY2))
        self.assertTrue(isfourcc(pixels.SDL_PIXELFORMAT_UYVY))
        self.assertTrue(isfourcc(pixels.SDL_PIXELFORMAT_YVYU))
        self.assertFalse(isfourcc(pixels.SDL_PIXELFORMAT_ARGB8888))
        self.assertFalse(isfourcc(pixels.SDL_PIXELFORMAT_ARGB4444))
        self.assertFalse(isfourcc(pixels.SDL_PIXELFORMAT_INDEX8))

    def test_SDL_GetPixelFormatName(self):
        self.assertEqual(pixels.SDL_GetPixelFormatName
                         (pixels.SDL_PIXELFORMAT_INDEX1LSB),
                         b"SDL_PIXELFORMAT_INDEX1LSB")
        self.assertEqual(pixels.SDL_GetPixelFormatName
                         (pixels.SDL_PIXELFORMAT_UNKNOWN),
                         b"SDL_PIXELFORMAT_UNKNOWN")
        self.assertEqual(pixels.SDL_GetPixelFormatName
                         (pixels.SDL_PIXELFORMAT_UYVY),
                         b"SDL_PIXELFORMAT_UYVY")
        self.assertEqual(pixels.SDL_GetPixelFormatName(99999),
                         b"SDL_PIXELFORMAT_UNKNOWN")

    def test_SDL_MasksToPixelFormatEnum(self):
        if sys.byteorder == "little":
            val = pixels.SDL_MasksToPixelFormatEnum(32,
                                                    0xFF000000,
                                                    0x00FF0000,
                                                    0x0000FF00,
                                                    0x000000FF)
        else:
            val = pixels.SDL_MasksToPixelFormatEnum(32,
                                                   0x000000FF,
                                                   0x0000FF00,
                                                   0x00FF0000,
                                                   0xFF000000)
        self.assertEqual(val, pixels.SDL_PIXELFORMAT_RGBA8888)
        if sys.byteorder == "little":
            val = pixels.SDL_MasksToPixelFormatEnum(32,
                                                   0xFF000000,
                                                   0x00FF0000,
                                                   0x0000FF00,
                                                   0)
        else:
            val = pixels.SDL_MasksToPixelFormatEnum(32,
                                                   0,
                                                   0x000000FF,
                                                   0x0000FF00,
                                                   0x00FF0000)
        self.assertEqual(val, pixels.SDL_PIXELFORMAT_RGBX8888)
        val = pixels.SDL_MasksToPixelFormatEnum(1, 0, 0, 0, 0)
        self.assertEqual(val, pixels.SDL_PIXELFORMAT_INDEX1MSB)  # not LSB
        val = pixels.SDL_MasksToPixelFormatEnum(17, 3, 6, 64, 255)
        self.assertEqual(val, pixels.SDL_PIXELFORMAT_UNKNOWN)
        val = pixels.SDL_MasksToPixelFormatEnum(0, 0, 0, 0, 0)
        self.assertEqual(val, pixels.SDL_PIXELFORMAT_UNKNOWN)

    def test_SDL_PixelFormatEnumToMasks(self):
        bpp = c_int()
        r, g, b, a = Uint32(), Uint32(), Uint32(), Uint32()
        pixels.SDL_PixelFormatEnumToMasks(pixels.SDL_PIXELFORMAT_INDEX1LSB,
                                          byref(bpp), byref(r), byref(g),
                                          byref(b), byref(a))
        self.assertEqual((bpp.value, r.value, g.value, b.value, a.value),
                         (1, 0, 0, 0, 0))
        pixels.SDL_PixelFormatEnumToMasks(pixels.SDL_PIXELFORMAT_INDEX1MSB,
                                          byref(bpp), byref(r), byref(g),
                                          byref(b), byref(a))
        self.assertEqual((bpp.value, r.value, g.value, b.value, a.value),
                         (1, 0, 0, 0, 0))

        pixels.SDL_PixelFormatEnumToMasks(pixels.SDL_PIXELFORMAT_RGBA8888,
                                          byref(bpp), byref(r), byref(g),
                                          byref(b), byref(a))
        if sys.byteorder == "little":
            self.assertEqual((bpp.value, r.value, g.value, b.value, a.value),
                             (32, 0xFF000000, 0x00FF0000, 0x0000FF00,
                              0x000000FF))
        else:
            self.assertEqual((bpp.value, r.value, g.value, b.value, a.value),
                             (32, 0x000000FF, 0x0000FF00, 0x00FF0000,
                              0xFF000000))
        pixels.SDL_PixelFormatEnumToMasks(pixels.SDL_PIXELFORMAT_RGBX8888,
                                          byref(bpp), byref(r),
                                          byref(g), byref(b),
                                          byref(a))
        if sys.byteorder == "little":
            self.assertEqual((bpp.value, r.value, g.value, b.value, a.value),
                             (32, 0xFF000000, 0x00FF0000, 0x0000FF00, 0))
        else:
            self.assertEqual((bpp.value, r.value, g.value, b.value, a.value),
                             (32, 0, 0x0000FF00, 0x00FF0000, 0xFF000000))
        # self.assertRaises(sdl.SDLError, pixels.SDL_PixelFormatEnumToMasks,
        #                   99999)

        pixels.SDL_PixelFormatEnumToMasks(0, byref(bpp), byref(r), byref(g),
                                          byref(b), byref(a))
        self.assertEqual((bpp.value, r.value, g.value, b.value, a.value),
                         (0, 0, 0, 0, 0))
        pixels.SDL_PixelFormatEnumToMasks(pixels.SDL_PIXELFORMAT_UNKNOWN,
                                          byref(bpp), byref(r), byref(g),
                                          byref(b), byref(a))
        self.assertEqual((bpp.value, r.value, g.value, b.value, a.value),
                         (0, 0, 0, 0, 0))

    def test_SDL_AllocFreeFormat(self):
        pformat = pixels.SDL_AllocFormat(pixels.SDL_PIXELFORMAT_RGBA8888)
        self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
        self.assertEqual(pformat.contents.format,
                         pixels.SDL_PIXELFORMAT_RGBA8888)
        self.assertEqual(pformat.contents.BitsPerPixel, 32)
        self.assertEqual(pformat.contents.BytesPerPixel, 4)
        pixels.SDL_FreeFormat(pformat)

        pformat = pixels.SDL_AllocFormat(pixels.SDL_PIXELFORMAT_INDEX1LSB)
        self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
        self.assertEqual(pformat.contents.format,
                         pixels.SDL_PIXELFORMAT_INDEX1LSB)
        self.assertEqual(pformat.contents.BitsPerPixel, 1)
        self.assertEqual(pformat.contents.BytesPerPixel, 1)
        pixels.SDL_FreeFormat(pformat)

        pformat = pixels.SDL_AllocFormat(pixels.SDL_PIXELFORMAT_INDEX4MSB)
        self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
        self.assertEqual(pformat.contents.format,
                         pixels.SDL_PIXELFORMAT_INDEX4MSB)
        self.assertEqual(pformat.contents.BitsPerPixel, 4)
        self.assertEqual(pformat.contents.BytesPerPixel, 1)
        pixels.SDL_FreeFormat(pformat)

        # self.assertRaises(sdl.SDLError, pixels.SDL_AllocFormat,
        #                   pixels.SDL_PIXELFORMAT_UYVY)
        # self.assertRaises(sdl.SDLError, pixels.SDL_AllocFormat,
        #                   pixels.SDL_PIXELFORMAT_YUY2)

    def test_SDL_AllocFreePalette(self):
        self.assertRaises((ArgumentError, TypeError), pixels.SDL_AllocPalette,
                          None)
        self.assertRaises((ArgumentError, TypeError), pixels.SDL_AllocPalette,
                          "Test")
        # self.assertRaises(ValueError, pixels.SDL_AllocPalette, -5)

        palette = pixels.SDL_AllocPalette(10)
        self.assertIsInstance(palette.contents, pixels.SDL_Palette)
        self.assertEqual(palette.contents.ncolors, 10)
        colors = palette.contents.colors
        for x in range(palette.contents.ncolors):
            self.assertIsInstance(colors[x], SDL_Color)
        colors[3].r = 70
        self.assertEqual(colors[3].r, 70)
        color = colors[4]
        self.assertEqual(colors[4].g, 255)
        self.assertEqual(color.g, 255)
        color.g = 33
        self.assertEqual(color.g, 33)
        self.assertEqual(colors[4].g, 33)
        pixels.SDL_FreePalette(palette)

    def test_SDL_CalculateGammaRamp(self):
        # TODO: more tests
        self.assertRaises(TypeError, pixels.SDL_CalculateGammaRamp, None)
        self.assertRaises(TypeError, pixels.SDL_CalculateGammaRamp, "Test")
        self.assertRaises(TypeError, pixels.SDL_CalculateGammaRamp, 7)
        self.assertRaises(TypeError, pixels.SDL_CalculateGammaRamp, -0.00002)
        vals = (Uint16 * 256)()
        pixels.SDL_CalculateGammaRamp(0, cast(vals, POINTER(Uint16)))
        self.assertEqual(len(vals), 256)
        for x in vals:
            self.assertEqual(x, 0)
        vals = (Uint16 * 256)()
        pixels.SDL_CalculateGammaRamp(1, cast(vals, POINTER(Uint16)))
        self.assertEqual(len(vals), 256)
        p = 0
        for x in vals:
            self.assertEqual(x, p)
            p += 257
        vals = (Uint16 * 256)()
        pixels.SDL_CalculateGammaRamp(0.5, cast(vals, POINTER(Uint16)))
        self.assertEqual(len(vals), 256)
        p, step = 0, 1
        for x in vals:
            if p == 33124:
                # dubios rounding correction - is this really correct?
                p = 33123
            self.assertEqual(x, p)
            p = x + step
            step += 2

    def test_SDL_GetRGB(self):
        # TODO: invalid parameters
        pformat = pixels.SDL_AllocFormat(pixels.SDL_PIXELFORMAT_RGBA8888)
        self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
        r, g, b = Uint8(), Uint8(), Uint8()
        pixels.SDL_GetRGB(0xFFAA8811, pformat, byref(r), byref(g), byref(b))
        self.assertEqual((r.value, g.value, b.value), (0xFF, 0xAA, 0x88))
        pixels.SDL_GetRGB(0x00000000, pformat, byref(r), byref(g), byref(b))
        self.assertEqual((r.value, g.value, b.value), (0x00, 0x00, 0x00))
        pixels.SDL_GetRGB(0xFFFFFFFF, pformat, byref(r), byref(g), byref(b))
        self.assertEqual((r.value, g.value, b.value), (0xFF, 0xFF, 0xFF))
        pixels.SDL_GetRGB(0x11223344, pformat, byref(r), byref(g), byref(b))
        self.assertEqual((r.value, g.value, b.value), (0x11, 0x22, 0x33))
        pixels.SDL_FreeFormat(pformat)
        fmts = (pixels.SDL_PIXELFORMAT_INDEX1LSB,
                pixels.SDL_PIXELFORMAT_INDEX1MSB)
        for fmt in fmts:
            pformat = pixels.SDL_AllocFormat(fmt)
            self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
            pixels.SDL_GetRGB(0x11223344, pformat, byref(r), byref(g),
                              byref(b))
            self.assertEqual((r.value, g.value, b.value), (0xFF, 0xFF, 0xFF))
            pixels.SDL_GetRGB(0x00000000, pformat, byref(r), byref(g),
                              byref(b))
            # TODO: Seems to be always (0xFF, 0xFF, 0xFF)???
            # self.assertEqual(rgb,(0x00, 0x00, 0x00))
            pixels.SDL_FreeFormat(pformat)
        fmts = (pixels.SDL_PIXELFORMAT_INDEX4LSB,
                pixels.SDL_PIXELFORMAT_INDEX4MSB)
        for fmt in fmts:
            pformat = pixels.SDL_AllocFormat(fmt)
            self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
            # TODO
            pixels.SDL_FreeFormat(pformat)

    def test_SDL_GetRGBA(self):
        # TODO: invalid parameters
        pformat = pixels.SDL_AllocFormat(pixels.SDL_PIXELFORMAT_RGBA8888)
        self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
        r, g, b, a = Uint8(), Uint8(), Uint8(), Uint8()
        pixels.SDL_GetRGBA(0xFFAA8811, pformat, byref(r), byref(g), byref(b),
                           byref(a))
        self.assertEqual((r.value, g.value, b.value, a.value),
                         (0xFF, 0xAA, 0x88, 0x11))
        pixels.SDL_GetRGBA(0x00000000, pformat, byref(r), byref(g), byref(b),
                           byref(a))
        self.assertEqual((r.value, g.value, b.value, a.value),
                         (0x00, 0x00, 0x00, 0x00))
        pixels.SDL_GetRGBA(0xFFFFFFFF, pformat, byref(r), byref(g), byref(b),
                           byref(a))
        self.assertEqual((r.value, g.value, b.value, a.value),
                         (0xFF, 0xFF, 0xFF, 0xFF))
        pixels.SDL_GetRGBA(0x11223344, pformat, byref(r), byref(g), byref(b),
                           byref(a))
        self.assertEqual((r.value, g.value, b.value, a.value),
                         (0x11, 0x22, 0x33, 0x44))
        pixels.SDL_FreeFormat(pformat)
        fmts = (pixels.SDL_PIXELFORMAT_INDEX1LSB,
                pixels.SDL_PIXELFORMAT_INDEX1MSB)
        for fmt in fmts:
            pformat = pixels.SDL_AllocFormat(fmt)
            self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
            pixels.SDL_GetRGBA(0x11223344, pformat, byref(r), byref(g),
                               byref(b), byref(a))
            self.assertEqual((r.value, g.value, b.value, a.value),
                             (0xFF, 0xFF, 0xFF, 0xFF))
            pixels.SDL_GetRGBA(0x00000000, pformat, byref(r), byref(g),
                               byref(b), byref(a))
            # TODO: Seems to be always(0xFF, 0xFF, 0xFF) ???
            # self.assertEqual(rgb,(0x00, 0x00, 0x00))
            pixels.SDL_FreeFormat(pformat)
        fmts = (pixels.SDL_PIXELFORMAT_INDEX4LSB,
                pixels.SDL_PIXELFORMAT_INDEX4MSB)
        for fmt in fmts:
            pformat = pixels.SDL_AllocFormat(fmt)
            self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
            # TODO
            pixels.SDL_FreeFormat(pformat)

    def test_SDL_MapRGB(self):
        pformat = pixels.SDL_AllocFormat(pixels.SDL_PIXELFORMAT_RGBA8888)
        self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
        val = pixels.SDL_MapRGB(pformat, 0xFF, 0xAA, 0x88)
        self.assertEqual(val, 0xFFAA88FF)
        pixels.SDL_FreeFormat(pformat)

        pformat = pixels.SDL_AllocFormat(pixels.SDL_PIXELFORMAT_UNKNOWN)
        self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
        self.assertEqual(pformat.contents.format,
                         pixels.SDL_PIXELFORMAT_UNKNOWN)
        val = pixels.SDL_MapRGB(pformat, 0xFF, 0xAA, 0x88)
        self.assertEqual(val, 0x0)
        pixels.SDL_FreeFormat(pformat)

    def test_SDL_MapRGBA(self):
        pformat = pixels.SDL_AllocFormat(pixels.SDL_PIXELFORMAT_RGBA8888)
        self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
        val = pixels.SDL_MapRGBA(pformat, 0xFF, 0xAA, 0x88, 0x11)
        self.assertEqual(val, 0xFFAA8811)
        pixels.SDL_FreeFormat(pformat)

        pformat = pixels.SDL_AllocFormat(pixels.SDL_PIXELFORMAT_UNKNOWN)
        self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
        self.assertEqual(pformat.contents.format,
                         pixels.SDL_PIXELFORMAT_UNKNOWN)
        val = pixels.SDL_MapRGBA(pformat, 0xFF, 0xAA, 0x88, 0x11)
        self.assertEqual(val, 0x0)
        pixels.SDL_FreeFormat(pformat)

    def test_SDL_SetPaletteColors(self):
        colors = []
        for v in range(20):
            colors.append(SDL_Color(v, v + 10, v + 20))

        palette = pixels.SDL_AllocPalette(10)
        self.assertIsInstance(palette.contents, pixels.SDL_Palette)
        self.assertEqual(palette.contents.ncolors, 10)
        colors = palette.contents.colors
        for index in range(10):
            rgb = colors[index]
            self.assertEqual((rgb.r, rgb.g, rgb.b), (255, 255, 255))
        pixels.SDL_SetPaletteColors(palette, colors, 0, 10)
        for index in range(10):
            rgb = palette.contents.colors[index]
            self.assertEqual(rgb, colors[index])
        pixels.SDL_SetPaletteColors(palette, colors, 5, 1000)
        for index in range(10):
            rgb = palette.contents.colors[index]
            if index < 5:
                self.assertEqual(rgb, colors[index])
            elif index > 5:
                self.assertEqual(rgb, colors[index - 5])

        pixels.SDL_FreePalette(palette)

    def test_SDL_SetPixelFormatPalette(self):
        palette = pixels.SDL_AllocPalette(10)
        self.assertIsInstance(palette.contents, pixels.SDL_Palette)
        pformat = pixels.SDL_AllocFormat(pixels.SDL_PIXELFORMAT_RGBA8888)
        self.assertIsInstance(pformat.contents, pixels.SDL_PixelFormat)
        pixels.SDL_SetPixelFormatPalette(pformat, palette)
        # TODO: improve tests
        pixels.SDL_FreeFormat(pformat)
        pixels.SDL_FreePalette(palette)

    def test_SDL_PixelFormat(self):
        # test_alloc_SDL_FreeFormat() contains the real tests
        pformat = pixels.SDL_PixelFormat()
        self.assertIsInstance(pformat, pixels.SDL_PixelFormat)

    def test_SDL_Palette(self):
        # test_alloc_SDL_FreePalette() contains the real tests
        palette = pixels.SDL_Palette()
        self.assertIsInstance(palette, pixels.SDL_Palette)

    def test_SDL_Color(self):
        c1 = SDL_Color()
        self.assertEqual((c1.r, c1.g, c1.b, c1.a), (0xFF, 0xFF, 0xFF, 0xFF))

        c1 = SDL_Color()
        c2 = SDL_Color()
        c3 = SDL_Color(0, 127, 255, 33)
        self.assertEqual(c1, c2)
        self.assertNotEqual(c1, c3)

    def test_SDL_Color__repr__(self):
        c1 = SDL_Color()
        self.assertEqual("SDL_Color(r=255, g=255, b=255, a=255)", repr(c1))
        c2 = eval(repr(c1))
        self.assertEqual(c2, c1)
        c3 = eval(repr(c2))
        self.assertEqual(c3, c2)

    def test_SDL_Color__copy__(self):
        c = SDL_Color()
        c2 = copy.copy(c)
        self.assertEqual(c, c2)

        c = SDL_Color(10, 20, 30)
        c2 = copy.copy(c)
        self.assertEqual(c, c2)

    def test_SDL_Color__eq__(self):
        self.assertTrue(SDL_Color(255, 0, 0, 0) == SDL_Color(255, 0, 0, 0))
        self.assertTrue(SDL_Color(0, 255, 0, 0) == SDL_Color(0, 255, 0, 0))
        self.assertTrue(SDL_Color(0, 0, 255, 0) == SDL_Color(0, 0, 255, 0))
        self.assertTrue(SDL_Color(0, 0, 0, 255) == SDL_Color(0, 0, 0, 255))
        self.assertTrue(SDL_Color(0, 0, 0, 0) == SDL_Color(0, 0, 0, 0))

        self.assertFalse(SDL_Color(0, 0, 0, 0) == SDL_Color(255, 0, 0, 0))
        self.assertFalse(SDL_Color(0, 0, 0, 0) == SDL_Color(0, 255, 0, 0))
        self.assertFalse(SDL_Color(0, 0, 0, 0) == SDL_Color(0, 0, 255, 0))
        self.assertFalse(SDL_Color(0, 0, 0, 0) == SDL_Color(0, 0, 0, 255))

    def test_SDL_Color__ne__(self):
        self.assertTrue(SDL_Color(0, 0, 0, 0) != SDL_Color(255, 0, 0, 0))
        self.assertTrue(SDL_Color(0, 0, 0, 0) != SDL_Color(0, 255, 0, 0))
        self.assertTrue(SDL_Color(0, 0, 0, 0) != SDL_Color(0, 0, 255, 0))
        self.assertTrue(SDL_Color(0, 0, 0, 0) != SDL_Color(0, 0, 255, 0))
        self.assertTrue(SDL_Color(0, 0, 0, 0) != SDL_Color(0, 0, 0, 255))

        self.assertFalse(SDL_Color(255, 0, 0, 0) != SDL_Color(255, 0, 0, 0))
        self.assertFalse(SDL_Color(0, 255, 0, 0) != SDL_Color(0, 255, 0, 0))
        self.assertFalse(SDL_Color(0, 0, 255, 0) != SDL_Color(0, 0, 255, 0))
        self.assertFalse(SDL_Color(0, 0, 0, 255) != SDL_Color(0, 0, 0, 255))

    def test_SDL_Color_r(self):
        c1 = SDL_Color()

        def setr(color, val):
            color.r = val

        for x in range(0, 255):
            c1.r = x
            self.assertEqual(c1.r, x)

        # TODO
        # self.assertRaises(ValueError, setr,  c1, -1)
        # self.assertRaises(ValueError, setr,  c1, 256)
        self.assertRaises(TypeError, setr, c1, "Test")
        self.assertRaises(TypeError, setr, c1, None)

    def test_SDL_Color_g(self):
        c1 = SDL_Color()

        def setg(color, val):
            color.g = val

        for x in range(0, 255):
            c1.g = x
            self.assertEqual(c1.g, x)

        # TODO
        # self.assertRaises(ValueError, setg,  c1, -1)
        # self.assertRaises(ValueError, setg,  c1, 256)
        self.assertRaises(TypeError, setg, c1, "Test")
        self.assertRaises(TypeError, setg, c1, None)

    def test_SDL_Color_b(self):
        c1 = SDL_Color()

        def setb(color, val):
            color.b = val

        for x in range(0, 255):
            c1.b = x
            self.assertEqual(c1.b, x)

        # TODO
        # self.assertRaises(ValueError, setb,  c1, -1)
        # self.assertRaises(ValueError, setb,  c1, 256)
        self.assertRaises(TypeError, setb, c1, "Test")
        self.assertRaises(TypeError, setb, c1, None)

    def test_SDL_Color_a(self):
        c1 = SDL_Color()

        def seta(color, val):
            color.a = val

        for x in range(0, 255):
            c1.a = x
            self.assertEqual(c1.a, x)

        # TODO
        # self.assertRaises(ValueError, seta,  c1, -1)
        # self.assertRaises(ValueError, seta,  c1, 256)
        self.assertRaises(TypeError, seta, c1, "Test")
        self.assertRaises(TypeError, seta, c1, None)


if __name__ == '__main__':
    sys.exit(unittest.main())
