# -*- coding: utf-8 -*-
import os
import sys
import unittest
from ctypes import byref, c_int, c_uint16
from sdl2 import SDL_Init, SDL_Quit, SDL_Color, surface, version, rwops

try:
    from sdl2 import sdlttf
    _HASSDLTTF=True
except:
    _HASSDLTTF=False

fontfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "resources", "tuffy.ttf").encode("utf-8")

@unittest.skipIf(not _HASSDLTTF, "SDL2_ttf library could not be loaded")
class SDLTTFTest(unittest.TestCase):
    __tags__ = ["sdl", "sdlttf"]

    @classmethod
    def setUpClass(cls):
        SDL_Init(0)
        sdlttf.TTF_Init()

    @classmethod
    def tearDownClass(cls):
        sdlttf.TTF_Quit()
        SDL_Quit()

    def test_TTF_Linked_Version(self):
        v = sdlttf.TTF_Linked_Version()
        self.assertIsInstance(v.contents, version.SDL_version)
        self.assertEqual(v.contents.major, 2)
        self.assertEqual(v.contents.minor, 0)
        self.assertGreaterEqual(v.contents.patch, 12)

    def test_TTF_Font(self):
        font = sdlttf.TTF_Font()
        self.assertIsInstance(font, sdlttf.TTF_Font)

    def test_TTF_InitQuit(self):
        sdlttf.TTF_Init()
        sdlttf.TTF_Init()
        sdlttf.TTF_Init()
        self.assertTrue(sdlttf.TTF_WasInit())
        sdlttf.TTF_Quit()
        sdlttf.TTF_Quit()
        self.assertFalse(sdlttf.TTF_WasInit())
        sdlttf.TTF_Init()
        self.assertTrue(sdlttf.TTF_WasInit())

    def test_TTF_OpenCloseFont(self):
        for x in range(6, 26):
            font = sdlttf.TTF_OpenFont(fontfile, x)
            self.assertIsInstance(font.contents, sdlttf.TTF_Font)
            sdlttf.TTF_CloseFont(font)
        #self.assertRaises(TypeError, sdlttf.open_font, None, None)
        #self.assertRaises(TypeError, sdlttf.open_font, filename, None)
        #self.assertRaises(ValueError, sdlttf.open_font, filename, "abcd")
        #self.assertRaises(ValueError, sdlttf.open_font, None, "abcd")
        #self.assertRaises(sdl.SDLError, sdlttf.open_font, "test", 10)

    def test_TTF_OpenFontIndex(self):
        for x in range(6, 26):
            font = sdlttf.TTF_OpenFontIndex(fontfile, x, 0)
            self.assertIsInstance(font.contents, sdlttf.TTF_Font)
            sdlttf.TTF_CloseFont(font)
        #self.assertRaises(TypeError, sdlttf.open_font_index, None, None, None)
        #self.assertRaises(TypeError, sdlttf.open_font_index, filename, None,
        #                  None)
        #self.assertRaises(TypeError, sdlttf.open_font_index, filename, 10,
        #                  None)
        #self.assertRaises(TypeError, sdlttf.open_font_index, filename, None,0)
        #self.assertRaises(TypeError, sdlttf.open_font_index, filename, None,0)
        #self.assertRaises(ValueError, sdlttf.open_font_index, filename, 10,-2)
        #self.assertRaises(sdl.SDLError, sdlttf.open_font_index, "test", 10, 0)

    def test_TTF_OpenFontRW(self):
        fp = open(fontfile, "rb")
        fontrw = rwops.rw_from_object(fp)
        for x in range(6, 26):
            fp.seek(0)
            font = sdlttf.TTF_OpenFontRW(fontrw, 0, x)
            self.assertIsInstance(font.contents, sdlttf.TTF_Font)
            sdlttf.TTF_CloseFont(font)
        fp.close()
        #self.assertRaises(TypeError, sdlttf.open_font_rw, None, False, None)
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.open_font_rw, None, False, 10)
        #self.assertRaises(TypeError, sdlttf.open_font_rw, fontrw, False, None)

    def test_TTF_OpenFontIndexRW(self):
        fp = open(fontfile, "rb")
        fontrw = rwops.rw_from_object(fp)
        for x in range(6, 26):
            fp.seek(0)
            font = sdlttf.TTF_OpenFontIndexRW(fontrw, 0, x, 0)
            self.assertIsInstance(font.contents, sdlttf.TTF_Font)
            sdlttf.TTF_CloseFont(font)
        fp.close()
        #self.assertRaises(TypeError, sdlttf.open_font_index_rw, None, False,
        #                  None, None)
        #self.assertRaises(TypeError, sdlttf.open_font_index_rw, None, False,
        #                 10, None)
        #self.assertRaises(TypeError, sdlttf.open_font_index_rw, None, False,
        #                  None, 0)
        #self.assertRaises(TypeError, sdlttf.open_font_index_rw, fontrw, False,
        #                  None, 0)
        #self.assertRaises(TypeError, sdlttf.open_font_index_rw, fontrw, False,
        #                  10, None)

    def test_TTF_GetSetFontStyle(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        self.assertIsInstance(font.contents, sdlttf.TTF_Font)
        self.assertEqual(sdlttf.TTF_GetFontStyle(font),
                         sdlttf.TTF_STYLE_NORMAL)
        sdlttf.TTF_SetFontStyle(font, sdlttf.TTF_STYLE_BOLD)
        self.assertEqual(sdlttf.TTF_GetFontStyle(font), sdlttf.TTF_STYLE_BOLD)
        sdlttf.TTF_SetFontStyle(font, sdlttf.TTF_STYLE_BOLD |
                                sdlttf.TTF_STYLE_ITALIC)
        self.assertEqual(sdlttf.TTF_GetFontStyle(font), sdlttf.TTF_STYLE_BOLD |
                         sdlttf.TTF_STYLE_ITALIC)
        sdlttf.TTF_SetFontStyle(font, sdlttf.TTF_STYLE_BOLD |
                                sdlttf.TTF_STYLE_UNDERLINE)
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.get_font_style, None)
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.get_font_style, "test")
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.get_font_style, 1234)
        #self.assertRaises(ArgumentError, sdlttf.set_font_style, font, None)
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.set_font_style, "test", None)
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.set_font_style, 1234, None)
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.set_font_style, "test", 3)
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.set_font_style, 1234, 4)
        #self.assertRaises(ArgumentError, sdlttf.set_font_style, font, "test")
        sdlttf.TTF_CloseFont(font)

    def test_TTF_GetSetFontOutline(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        self.assertEqual(sdlttf.TTF_GetFontOutline(font), 0)
        for x in range(1, 11):
            sdlttf.TTF_SetFontOutline(font, x)
            self.assertEqual(sdlttf.TTF_GetFontOutline(font), x)
        #self.assertRaises(TypeError, sdlttf.set_font_outline, None, None)
        #self.assertRaises(TypeError, sdlttf.set_font_outline, font, None)
        #self.assertRaises(ValueError, sdlttf.set_font_outline, font, "test")
        #self.assertRaises(ValueError, sdlttf.set_font_outline, None, "test")
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.set_font_outline, None, 123)
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.get_font_outline, None)
        #self.assertRaises((AttributeError, TypeError),
        #                  sdlttf.get_font_outline, None)
        sdlttf.TTF_CloseFont(font)

    def test_TTF_GetSetFontHinting(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        self.assertEqual(sdlttf.TTF_GetFontHinting(font),
                         sdlttf.TTF_HINTING_NORMAL)
        for hint in (sdlttf.TTF_HINTING_NORMAL, sdlttf.TTF_HINTING_LIGHT,
                     sdlttf.TTF_HINTING_MONO, sdlttf.TTF_HINTING_NONE):
            sdlttf.TTF_SetFontHinting(font, hint)
            self.assertEqual(sdlttf.TTF_GetFontHinting(font), hint)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.set_font_hinting, None, None)
#        self.assertRaises(ArgumentError, sdlttf.set_font_hinting, font, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.set_font_hinting, None, 1)
#        self.assertRaises(ArgumentError, sdlttf.set_font_hinting, font,"test")
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.set_font_hinting, None, "test")
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.get_font_hinting, None)
        sdlttf.TTF_CloseFont(font)

    def test_TTF_FontHeight(self):
        last = cur = 0
        for ptsize in range(6, 26):
            font = sdlttf.TTF_OpenFont(fontfile, ptsize)
            cur = sdlttf.TTF_FontHeight(font)
            self.assertGreaterEqual(cur, last)
            last = cur
            sdlttf.TTF_CloseFont(font)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_height, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_height, 1234)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_height, "test")

    def test_TTF_FontAscent(self):
        last = cur = 0
        for ptsize in range(6, 26):
            font = sdlttf.TTF_OpenFont(fontfile, ptsize)
            cur = sdlttf.TTF_FontAscent(font)
            self.assertGreaterEqual(cur, last)
            last = cur
            sdlttf.TTF_CloseFont(font)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_ascent, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_ascent, 1234)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_ascent, "test")

    def test_TTF_FontDescent(self):
        last = cur = 0
        for ptsize in range(6, 26):
            font = sdlttf.TTF_OpenFont(fontfile, ptsize)
            cur = sdlttf.TTF_FontDescent(font)
            self.assertLessEqual(cur, last)
            last = cur
            sdlttf.TTF_CloseFont(font)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_descent, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_descent, 1234)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_descent, "test")

    def test_TTF_FontLineSkip(self):
        last = cur = 0
        for ptsize in range(6, 26):
            font = sdlttf.TTF_OpenFont(fontfile, ptsize)
            cur = sdlttf.TTF_FontLineSkip(font)
            self.assertGreaterEqual(cur, last)
            last = cur
            sdlttf.TTF_CloseFont(font)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_line_skip, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_line_skip, 1234)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_line_skip, "test")

    def test_TTF_GetSetFontKerning(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        self.assertEqual(sdlttf.TTF_GetFontKerning(font), 1)
        sdlttf.TTF_SetFontKerning(font, 0)
        self.assertEqual(sdlttf.TTF_GetFontKerning(font), 0)
        sdlttf.TTF_SetFontKerning(font, 1)
        self.assertEqual(sdlttf.TTF_GetFontKerning(font), 1)
        sdlttf.TTF_SetFontKerning(font, 0)
        self.assertEqual(sdlttf.TTF_GetFontKerning(font), 0)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.get_font_kerning, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.get_font_kerning, "test")
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.get_font_kerning, 1234)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.set_font_kerning, None, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.set_font_kerning, "test", "test")
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.set_font_kerning, 1234, None)
        sdlttf.TTF_CloseFont(font)

    @unittest.skip("not implemented")
    def test_TTF_GetFontKerningSizeGlyphs(self):
        pass

    def test_TTF_FontFaces(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        self.assertGreaterEqual(sdlttf.TTF_FontFaces(font), 1)
#        self.assertRaises((AttributeError, TypeError), sdlttf.font_faces,None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_faces, "test")
#        self.assertRaises((AttributeError, TypeError), sdlttf.font_faces,1234)
        sdlttf.TTF_CloseFont(font)

    def test_TTF_FontFaceIsFixedWidth(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        self.assertFalse(sdlttf.TTF_FontFaceIsFixedWidth(font))
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_face_is_fixed_width, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_face_is_fixed_width, "test")
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_face_is_fixed_width, 1234)
        sdlttf.TTF_CloseFont(font)

    def test_TTF_FontFaceFamilyName(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        self.assertEqual(sdlttf.TTF_FontFaceFamilyName(font), b"Tuffy")
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_face_family_name, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_face_family_name, "test")
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_face_family_name, 1234)
        sdlttf.TTF_CloseFont(font)

    def test_TTF_FontFaceStyleName(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        self.assertEqual(sdlttf.TTF_FontFaceStyleName(font), b"Regular")
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_face_style_name, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_face_style_name, "test")
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.font_face_style_name, 1234)
        sdlttf.TTF_CloseFont(font)

    def test_TTF_GlyphIsProvided(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        self.assertIsInstance(font.contents, sdlttf.TTF_Font)
        for ch in range(32, 127):
            self.assertTrue(sdlttf.TTF_GlyphIsProvided(font, ch))
        self.assertFalse(sdlttf.TTF_GlyphIsProvided(font, 0))
        self.assertFalse(sdlttf.TTF_GlyphIsProvided(font, 0x0ff9))
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.glyph_is_provided, None, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.glyph_is_provided, "test", None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.glyph_is_provided, "test", 1234)
#        self.assertRaises((ArgumentError, TypeError),
#                          sdlttf.glyph_is_provided, font, None)
#        self.assertRaises((AttributeError, TypeError),
#                          sdlttf.glyph_is_provided, font, "test")

    def test_TTF_GlyphMetrics(self):
        expected = {
            'A': [1, 25, 0, 29, 25],
            'j': [-3, 7, -9, 28, 9],
            '.': [2, 7, -1, 4, 8]
        }
        font = sdlttf.TTF_OpenFont(fontfile, 40)
        minX, maxX, minY, maxY = c_int(0), c_int(0), c_int(0), c_int(0)
        adv = c_int(0)
        for char in expected.keys():
            sdlttf.TTF_GlyphMetrics(
                font, ord(char),
                byref(minX), byref(maxX), byref(minY), byref(maxY), byref(adv)
            )
            results = [x.value for x in (minX, maxX, minY, maxY, adv)]
            self.assertListEqual(results, expected[char])
        sdlttf.TTF_CloseFont(font)

    def test_TTF_Size(self):
        font = sdlttf.TTF_OpenFont(fontfile, 20)
        w, h = c_int(0), c_int(0)
        # Test TTF_SizeText
        sdlttf.TTF_SizeText(font, b"Hi there!", w, h)
        self.assertListEqual([w.value, h.value], [70, 21])
        # Test TTF_SizeUTF8
        sdlttf.TTF_SizeUTF8(font, u"Hï thère!".encode('utf-8'), w, h)
        self.assertListEqual([w.value, h.value], [70, 21])
        # Test TTF_SizeUNICODE
        # NOTE: no unicode chars because number -> glyph lookup is os-dependent
        teststr = b"Hi there!"
        strarr = (c_uint16 * len(teststr))()
        strarr[:] = teststr
        sdlttf.TTF_SizeUNICODE(font, strarr, w, h)
        self.assertListEqual([w.value, h.value], [70, 21])
        sdlttf.TTF_CloseFont(font)

    def test_TTF_Render_Solid(self):
        font = sdlttf.TTF_OpenFont(fontfile, 20)
        color = SDL_Color(0, 0, 0)
        # Test TTF_RenderText_Solid
        sf = sdlttf.TTF_RenderText_Solid(font, b"Hi there!", color)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUTF8_Solid
        teststr = u"Hï thère!".encode('utf-8')
        sf = sdlttf.TTF_RenderUTF8_Solid(font, teststr, color)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUNICODE_Solid
        # NOTE: no unicode chars because number -> glyph lookup is os-dependent
        teststr = b"Hi there!"
        strarr = (c_uint16 * len(teststr))()
        strarr[:] = teststr
        sf = sdlttf.TTF_RenderUNICODE_Solid(font, teststr, color)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderGlyph_Solid
        sf = sdlttf.TTF_RenderGlyph_Solid(font, ord("A"), color)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        sdlttf.TTF_CloseFont(font)

    def test_TTF_Render_Shaded(self):
        font = sdlttf.TTF_OpenFont(fontfile, 20)
        color = SDL_Color(0, 0, 0)
        bgcolor = SDL_Color(255, 255, 255)
        # Test TTF_RenderText_Shaded
        sf = sdlttf.TTF_RenderText_Shaded(font, b"Hi there!", color, bgcolor)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUTF8_Shaded
        teststr = u"Hï thère!".encode('utf-8')
        sf = sdlttf.TTF_RenderUTF8_Shaded(font, teststr, color, bgcolor)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUNICODE_Shaded
        # NOTE: no unicode chars because number -> glyph lookup is os-dependent
        teststr = b"Hi there!"
        strarr = (c_uint16 * len(teststr))()
        strarr[:] = teststr
        sf = sdlttf.TTF_RenderUNICODE_Shaded(font, teststr, color, bgcolor)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderGlyph_Solid
        sf = sdlttf.TTF_RenderGlyph_Shaded(font, ord("A"), color, bgcolor)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        sdlttf.TTF_CloseFont(font)

    def test_TTF_Render_Blended(self):
        font = sdlttf.TTF_OpenFont(fontfile, 20)
        color = SDL_Color(0, 0, 0, 255)
        # Test TTF_RenderText_Blended
        sf = sdlttf.TTF_RenderText_Blended(font, b"Hi there!", color)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUTF8_Blended
        teststr = u"Hï thère!".encode('utf-8')
        sf = sdlttf.TTF_RenderUTF8_Blended(font, teststr, color)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUNICODE_Blended
        # NOTE: no unicode chars because number -> glyph lookup is os-dependent
        teststr = b"Hi there!"
        strarr = (c_uint16 * len(teststr))()
        strarr[:] = teststr
        sf = sdlttf.TTF_RenderUNICODE_Blended(font, teststr, color)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderGlyph_Solid
        sf = sdlttf.TTF_RenderGlyph_Blended(font, ord("A"), color)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        sdlttf.TTF_CloseFont(font)

    @unittest.skip("not implemented")
    def test_TTF_Render_Blended_Wrapped(self):
        # TODO: Add tests for TTF_RenderText_Blended_Wrapped,
        # TTF_RenderUTF8_Blended_Wrapped, and TTF_RenderUNICODE_Blended_Wrapped
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
