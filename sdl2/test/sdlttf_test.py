# -*- coding: utf-8 -*-
import os
import sys
import pytest
from struct import unpack
from ctypes import byref, c_int, c_uint16
from sdl2 import SDL_Init, SDL_Quit, SDL_Color, surface, version, rwops

sdlttf = pytest.importorskip("sdl2.sdlttf")


fontfile = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "resources", "tuffy.ttf").encode("utf-8")

class TestSDLTTF(object):
    __tags__ = ["sdl", "sdlttf"]

    @classmethod
    def setup_class(cls):
        SDL_Init(0)
        sdlttf.TTF_Init()

    @classmethod
    def teardown_class(cls):
        sdlttf.TTF_Quit()
        SDL_Quit()

    def test_TTF_Linked_Version(self):
        v = sdlttf.TTF_Linked_Version()
        assert isinstance(v.contents, version.SDL_version)
        assert v.contents.major == 2
        assert v.contents.minor == 0
        assert v.contents.patch >= 12

    def test_TTF_Font(self):
        font = sdlttf.TTF_Font()
        assert isinstance(font, sdlttf.TTF_Font)

    def test_TTF_InitQuit(self):
        # Every time TTF_Init() is run, internal number increments by 1,
        # every time TTF_Quit() is run, internal number decrements by 1 and
        # only actually quits when internal number == 0
        sdlttf.TTF_Init()
        sdlttf.TTF_Init()
        assert sdlttf.TTF_WasInit()
        sdlttf.TTF_Quit()
        sdlttf.TTF_Quit()
        sdlttf.TTF_Quit()
        assert not sdlttf.TTF_WasInit()
        sdlttf.TTF_Init()
        assert sdlttf.TTF_WasInit()

    def test_TTF_OpenCloseFont(self):
        for x in range(6, 26):
            font = sdlttf.TTF_OpenFont(fontfile, x)
            assert isinstance(font.contents, sdlttf.TTF_Font)
            sdlttf.TTF_CloseFont(font)

    def test_TTF_OpenFontIndex(self):
        for x in range(6, 26):
            font = sdlttf.TTF_OpenFontIndex(fontfile, x, 0)
            assert isinstance(font.contents, sdlttf.TTF_Font)
            sdlttf.TTF_CloseFont(font)

    def test_TTF_OpenFontRW(self):
        fp = open(fontfile, "rb")
        fontrw = rwops.rw_from_object(fp)
        for x in range(6, 26):
            fp.seek(0)
            font = sdlttf.TTF_OpenFontRW(fontrw, 0, x)
            assert isinstance(font.contents, sdlttf.TTF_Font)
            sdlttf.TTF_CloseFont(font)
        fp.close()

    def test_TTF_OpenFontIndexRW(self):
        fp = open(fontfile, "rb")
        fontrw = rwops.rw_from_object(fp)
        for x in range(6, 26):
            fp.seek(0)
            font = sdlttf.TTF_OpenFontIndexRW(fontrw, 0, x, 0)
            assert isinstance(font.contents, sdlttf.TTF_Font)
            sdlttf.TTF_CloseFont(font)
        fp.close()

    def test_TTF_GetSetFontStyle(self):
        normal = sdlttf.TTF_STYLE_NORMAL
        bold = sdlttf.TTF_STYLE_BOLD
        italic = sdlttf.TTF_STYLE_ITALIC
        underline = sdlttf.TTF_STYLE_UNDERLINE
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        assert isinstance(font.contents, sdlttf.TTF_Font)
        assert sdlttf.TTF_GetFontStyle(font) == normal
        sdlttf.TTF_SetFontStyle(font, bold)
        assert sdlttf.TTF_GetFontStyle(font) == bold
        sdlttf.TTF_SetFontStyle(font, bold | italic)
        assert sdlttf.TTF_GetFontStyle(font) == bold | italic
        sdlttf.TTF_SetFontStyle(font, bold | underline)
        assert sdlttf.TTF_GetFontStyle(font) == bold | underline
        sdlttf.TTF_CloseFont(font)

    def test_TTF_GetSetFontOutline(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        assert sdlttf.TTF_GetFontOutline(font) == 0
        for x in range(1, 11):
            sdlttf.TTF_SetFontOutline(font, x)
            assert sdlttf.TTF_GetFontOutline(font) == x
        sdlttf.TTF_CloseFont(font)

    def test_TTF_GetSetFontHinting(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        assert sdlttf.TTF_GetFontHinting(font) == sdlttf.TTF_HINTING_NORMAL
        for hint in (sdlttf.TTF_HINTING_NORMAL, sdlttf.TTF_HINTING_LIGHT,
                     sdlttf.TTF_HINTING_MONO, sdlttf.TTF_HINTING_NONE):
            sdlttf.TTF_SetFontHinting(font, hint)
            assert sdlttf.TTF_GetFontHinting(font) == hint
        sdlttf.TTF_CloseFont(font)

    def test_TTF_FontHeight(self):
        last = cur = 0
        for ptsize in range(6, 26):
            font = sdlttf.TTF_OpenFont(fontfile, ptsize)
            cur = sdlttf.TTF_FontHeight(font)
            assert cur >= last
            last = cur
            sdlttf.TTF_CloseFont(font)

    def test_TTF_FontAscent(self):
        last = cur = 0
        for ptsize in range(6, 26):
            font = sdlttf.TTF_OpenFont(fontfile, ptsize)
            cur = sdlttf.TTF_FontAscent(font)
            assert cur >= last
            last = cur
            sdlttf.TTF_CloseFont(font)

    def test_TTF_FontDescent(self):
        last = cur = 0
        for ptsize in range(6, 26):
            font = sdlttf.TTF_OpenFont(fontfile, ptsize)
            cur = sdlttf.TTF_FontDescent(font)
            assert cur <= last
            last = cur
            sdlttf.TTF_CloseFont(font)

    def test_TTF_FontLineSkip(self):
        last = cur = 0
        for ptsize in range(6, 26):
            font = sdlttf.TTF_OpenFont(fontfile, ptsize)
            cur = sdlttf.TTF_FontLineSkip(font)
            assert cur >= last
            last = cur
            sdlttf.TTF_CloseFont(font)

    def test_TTF_GetSetFontKerning(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        assert sdlttf.TTF_GetFontKerning(font) == 1
        sdlttf.TTF_SetFontKerning(font, 0)
        assert sdlttf.TTF_GetFontKerning(font) == 0
        sdlttf.TTF_SetFontKerning(font, 1)
        assert sdlttf.TTF_GetFontKerning(font) == 1
        sdlttf.TTF_SetFontKerning(font, 0)
        assert sdlttf.TTF_GetFontKerning(font) == 0
        sdlttf.TTF_CloseFont(font)

    @pytest.mark.skip("not implemented")
    def test_TTF_GetFontKerningSizeGlyphs(self):
        pass

    def test_TTF_FontFaces(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        assert sdlttf.TTF_FontFaces(font) >= 1
        sdlttf.TTF_CloseFont(font)

    def test_TTF_FontFaceIsFixedWidth(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        assert not sdlttf.TTF_FontFaceIsFixedWidth(font)
        sdlttf.TTF_CloseFont(font)

    def test_TTF_FontFaceFamilyName(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        assert sdlttf.TTF_FontFaceFamilyName(font) == b"Tuffy"
        sdlttf.TTF_CloseFont(font)

    def test_TTF_FontFaceStyleName(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        assert sdlttf.TTF_FontFaceStyleName(font) == b"Regular"
        sdlttf.TTF_CloseFont(font)

    def test_TTF_GlyphIsProvided(self):
        font = sdlttf.TTF_OpenFont(fontfile, 10)
        assert isinstance(font.contents, sdlttf.TTF_Font)
        for ch in range(32, 127):
            assert sdlttf.TTF_GlyphIsProvided(font, ch)
        assert not sdlttf.TTF_GlyphIsProvided(font, 0)
        assert not sdlttf.TTF_GlyphIsProvided(font, 0x0ff9)
        sdlttf.TTF_CloseFont(font)

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
            assert results == expected[char]
        sdlttf.TTF_CloseFont(font)

    def test_TTF_SizeText(self):
        font = sdlttf.TTF_OpenFont(fontfile, 20)
        expected_w = 70
        expected_h = [
            25, # SDL2_ttf < 2.0.15
            24, # SDL2_ttf == 2.0.15 w/ FreeType 2.9.1
            21  # SDL2_ttf == 2.0.15 w/ FreeType 2.10.1
        ]
        w, h = c_int(0), c_int(0)
        sdlttf.TTF_SizeText(font, b"Hi there!", byref(w), byref(h))
        assert w.value == expected_w
        assert h.value in expected_h
        sdlttf.TTF_CloseFont(font)

    def test_TTF_SizeUTF8(self):
        font = sdlttf.TTF_OpenFont(fontfile, 20)
        expected_w = 73
        expected_h = [
            25, # SDL2_ttf < 2.0.15
            24, # SDL2_ttf == 2.0.15 w/ FreeType 2.9.1
            21  # SDL2_ttf == 2.0.15 w/ FreeType 2.10.1
        ]
        w, h = c_int(0), c_int(0)
        sdlttf.TTF_SizeUTF8(font, u"Hï thère!".encode('utf-8'), byref(w), byref(h))
        assert w.value == expected_w
        assert h.value in expected_h
        sdlttf.TTF_CloseFont(font)

    @pytest.mark.xfail(reason="Highly unstable under pytest for some reason")
    def test_TTF_SizeUNICODE(self):
        font = sdlttf.TTF_OpenFont(fontfile, 20)
        expected_w = 70
        expected_h = [
            25, # SDL2_ttf < 2.0.15
            24, # SDL2_ttf == 2.0.15 w/ FreeType 2.9.1
            21  # SDL2_ttf == 2.0.15 w/ FreeType 2.10.1
        ]
        w, h = c_int(0), c_int(0)
        teststr = u"Hi there!"
        strlen = len(teststr) + 1 # +1 for byte-order mark
        intstr = unpack('H' * strlen, teststr.encode('utf-16'))
        strarr = (c_uint16 * strlen)(*intstr)
        sdlttf.TTF_SizeUNICODE(font, strarr, byref(w), byref(h))
        print(list(strarr))
        print("w = {0}, h = {1}".format(w.value, h.value))
        assert w.value == expected_w
        assert h.value in expected_h
        sdlttf.TTF_CloseFont(font)

    def test_TTF_Render_Solid(self):
        font = sdlttf.TTF_OpenFont(fontfile, 20)
        color = SDL_Color(0, 0, 0)
        # Test TTF_RenderText_Solid
        sf = sdlttf.TTF_RenderText_Solid(font, b"Hi there!", color)
        assert isinstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUTF8_Solid
        teststr = u"Hï thère!".encode('utf-8')
        sf = sdlttf.TTF_RenderUTF8_Solid(font, teststr, color)
        assert isinstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUNICODE_Solid
        # NOTE: no unicode chars because number -> glyph lookup is os-dependent
        teststr = u"Hi there!"
        strlen = len(teststr) + 1 # +1 for byte-order mark
        intstr = unpack('H' * strlen, teststr.encode('utf-16'))
        strarr = (c_uint16 * strlen)(*intstr)
        sf = sdlttf.TTF_RenderUNICODE_Solid(font, strarr, color)
        assert isinstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderGlyph_Solid
        sf = sdlttf.TTF_RenderGlyph_Solid(font, ord("A"), color)
        assert isinstance(sf.contents, surface.SDL_Surface)

    def test_TTF_Render_Shaded(self):
        font = sdlttf.TTF_OpenFont(fontfile, 20)
        color = SDL_Color(0, 0, 0)
        bgcolor = SDL_Color(255, 255, 255)
        # Test TTF_RenderText_Shaded
        sf = sdlttf.TTF_RenderText_Shaded(font, b"Hi there!", color, bgcolor)
        assert isinstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUTF8_Shaded
        teststr = u"Hï thère!".encode('utf-8')
        sf = sdlttf.TTF_RenderUTF8_Shaded(font, teststr, color, bgcolor)
        assert isinstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUNICODE_Shaded
        # NOTE: no unicode chars because number -> glyph lookup is os-dependent
        teststr = u"Hi there!"
        strlen = len(teststr) + 1 # +1 for byte-order mark
        intstr = unpack('H' * strlen, teststr.encode('utf-16'))
        strarr = (c_uint16 * strlen)(*intstr)
        sf = sdlttf.TTF_RenderUNICODE_Shaded(font, strarr, color, bgcolor)
        assert isinstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderGlyph_Solid
        sf = sdlttf.TTF_RenderGlyph_Shaded(font, ord("A"), color, bgcolor)
        assert isinstance(sf.contents, surface.SDL_Surface)
        sdlttf.TTF_CloseFont(font)

    def test_TTF_Render_Blended(self):
        font = sdlttf.TTF_OpenFont(fontfile, 20)
        color = SDL_Color(0, 0, 0, 255)
        # Test TTF_RenderText_Blended
        sf = sdlttf.TTF_RenderText_Blended(font, b"Hi there!", color)
        assert isinstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUTF8_Blended
        teststr = u"Hï thère!".encode('utf-8')
        sf = sdlttf.TTF_RenderUTF8_Blended(font, teststr, color)
        assert isinstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderUNICODE_Blended
        # NOTE: no unicode chars because number -> glyph lookup is os-dependent
        teststr = u"Hi there!"
        strlen = len(teststr) + 1 # +1 for byte-order mark
        intstr = unpack('H' * strlen, teststr.encode('utf-16'))
        strarr = (c_uint16 * strlen)(*intstr)
        sf = sdlttf.TTF_RenderUNICODE_Blended(font, strarr, color)
        assert isinstance(sf.contents, surface.SDL_Surface)
        # Test TTF_RenderGlyph_Solid
        sf = sdlttf.TTF_RenderGlyph_Blended(font, ord("A"), color)
        assert isinstance(sf.contents, surface.SDL_Surface)
        sdlttf.TTF_CloseFont(font)

    @pytest.mark.skip("not implemented")
    def test_TTF_Render_Blended_Wrapped(self):
        # TODO: Add tests for TTF_RenderText_Blended_Wrapped,
        # TTF_RenderUTF8_Blended_Wrapped, and TTF_RenderUNICODE_Blended_Wrapped
        pass
