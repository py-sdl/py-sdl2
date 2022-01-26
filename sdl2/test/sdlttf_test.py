# -*- coding: utf-8 -*-
import os
import gc
import pytest
from struct import unpack
from ctypes import byref, c_int, c_uint16
import sdl2
from sdl2 import SDL_Init, SDL_Quit, SDL_Color, surface, version, rwops

sdlttf = pytest.importorskip("sdl2.sdlttf")

parent_dir = os.path.dirname(os.path.abspath(__file__))
fontfile = os.path.join(parent_dir, "resources", "tuffy.ttf").encode("utf-8")
font_test_sizes = [6, 16, 26]

@pytest.fixture(scope="module")
def with_sdl_ttf(with_sdl):
    ret = sdlttf.TTF_Init()
    assert sdlttf.TTF_GetError() == b""
    assert ret == 0
    yield
    while sdlttf.TTF_WasInit() > 0:
        sdlttf.TTF_Quit()

@pytest.fixture()
def with_font(with_sdl_ttf):
    sdl2.SDL_ClearError()
    font = sdlttf.TTF_OpenFont(fontfile, 20)
    assert sdlttf.TTF_GetError() == b""
    assert font
    yield font
    sdlttf.TTF_CloseFont(font)
    gc.collect()


def test_TTF_Font():
    font = sdlttf.TTF_Font()
    assert isinstance(font, sdlttf.TTF_Font)

def test_TTF_InitQuit(with_sdl):
    # Test that init and quit actually work
    ret = sdlttf.TTF_Init()
    assert sdlttf.TTF_GetError() == b""
    assert ret == 0
    assert sdlttf.TTF_WasInit()
    sdlttf.TTF_Quit()
    assert not sdlttf.TTF_WasInit()
    # Every time TTF_Init() is run, internal number increments by 1,
    # every time TTF_Quit() is run, internal number decrements by 1 and
    # only actually quits when internal number == 0
    sdlttf.TTF_Init()
    sdlttf.TTF_Init()
    sdlttf.TTF_Quit()
    assert sdlttf.TTF_WasInit()
    sdlttf.TTF_Quit()
    assert not sdlttf.TTF_WasInit()

def test_TTF_Linked_Version(with_sdl_ttf):
    v = sdlttf.TTF_Linked_Version()
    assert isinstance(v.contents, version.SDL_version)
    assert v.contents.major == 2
    assert v.contents.minor == 0
    assert v.contents.patch >= 12

def test_TTF_ByteSwappedUNICODE(with_sdl_ttf):
    sdlttf.TTF_ByteSwappedUNICODE(0)
    sdlttf.TTF_ByteSwappedUNICODE(1)

def test_TTF_OpenCloseFont(with_sdl_ttf):
    for x in font_test_sizes:
        font = sdlttf.TTF_OpenFont(fontfile, x)
        assert sdlttf.TTF_GetError() == b""
        assert isinstance(font.contents, sdlttf.TTF_Font)
        sdlttf.TTF_CloseFont(font)

def test_TTF_OpenFontIndex(with_sdl_ttf):
    for x in font_test_sizes:
        font = sdlttf.TTF_OpenFontIndex(fontfile, x, 0)
        assert sdlttf.TTF_GetError() == b""
        assert isinstance(font.contents, sdlttf.TTF_Font)
        sdlttf.TTF_CloseFont(font)

def test_TTF_OpenFontRW(with_sdl_ttf):
    fp = open(fontfile, "rb")
    fontrw = rwops.rw_from_object(fp)
    for x in font_test_sizes:
        fp.seek(0)
        font = sdlttf.TTF_OpenFontRW(fontrw, 0, x)
        assert sdlttf.TTF_GetError() == b""
        assert isinstance(font.contents, sdlttf.TTF_Font)
        sdlttf.TTF_CloseFont(font)
    fp.close()

def test_TTF_OpenFontIndexRW(with_sdl_ttf):
    fp = open(fontfile, "rb")
    fontrw = rwops.rw_from_object(fp)
    for x in font_test_sizes:
        fp.seek(0)
        font = sdlttf.TTF_OpenFontIndexRW(fontrw, 0, x, 0)
        assert sdlttf.TTF_GetError() == b""
        assert isinstance(font.contents, sdlttf.TTF_Font)
        sdlttf.TTF_CloseFont(font)
    fp.close()

def test_TTF_GetSetFontStyle(with_font):
    normal = sdlttf.TTF_STYLE_NORMAL
    bold = sdlttf.TTF_STYLE_BOLD
    italic = sdlttf.TTF_STYLE_ITALIC
    underline = sdlttf.TTF_STYLE_UNDERLINE
    # Test out getting/setting different font styles
    font = with_font
    assert sdlttf.TTF_GetFontStyle(font) == normal
    sdlttf.TTF_SetFontStyle(font, bold)
    assert sdlttf.TTF_GetFontStyle(font) == bold
    sdlttf.TTF_SetFontStyle(font, bold | italic)
    assert sdlttf.TTF_GetFontStyle(font) == bold | italic
    sdlttf.TTF_SetFontStyle(font, bold | underline)
    assert sdlttf.TTF_GetFontStyle(font) == bold | underline

def test_TTF_GetSetFontOutline(with_font):
    font = with_font
    assert sdlttf.TTF_GetFontOutline(font) == 0
    for x in range(1, 11, 2):
        sdlttf.TTF_SetFontOutline(font, x)
        assert sdlttf.TTF_GetFontOutline(font) == x

def test_TTF_GetSetFontHinting(with_font):
    font = with_font
    hints = [
        sdlttf.TTF_HINTING_NORMAL, sdlttf.TTF_HINTING_LIGHT,
        sdlttf.TTF_HINTING_MONO, sdlttf.TTF_HINTING_NONE
    ]
    assert sdlttf.TTF_GetFontHinting(font) == sdlttf.TTF_HINTING_NORMAL
    for hint in hints:
        sdlttf.TTF_SetFontHinting(font, hint)
        assert sdlttf.TTF_GetFontHinting(font) == hint

def test_TTF_FontHeight(with_sdl_ttf):
    last = cur = 0
    for ptsize in font_test_sizes:
        font = sdlttf.TTF_OpenFont(fontfile, ptsize)
        cur = sdlttf.TTF_FontHeight(font)
        assert cur >= last
        last = cur
        sdlttf.TTF_CloseFont(font)

def test_TTF_FontAscent(with_sdl_ttf):
    last = cur = 0
    for ptsize in font_test_sizes:
        font = sdlttf.TTF_OpenFont(fontfile, ptsize)
        cur = sdlttf.TTF_FontAscent(font)
        assert cur >= last
        last = cur
        sdlttf.TTF_CloseFont(font)

def test_TTF_FontDescent(with_sdl_ttf):
    last = cur = 0
    for ptsize in font_test_sizes:
        font = sdlttf.TTF_OpenFont(fontfile, ptsize)
        cur = sdlttf.TTF_FontDescent(font)
        assert cur <= last
        last = cur
        sdlttf.TTF_CloseFont(font)

def test_TTF_FontLineSkip(with_sdl_ttf):
    last = cur = 0
    for ptsize in font_test_sizes:
        font = sdlttf.TTF_OpenFont(fontfile, ptsize)
        cur = sdlttf.TTF_FontLineSkip(font)
        assert cur >= last
        last = cur
        sdlttf.TTF_CloseFont(font)

def test_TTF_GetSetFontKerning(with_font):
    font = with_font
    assert sdlttf.TTF_GetFontKerning(font) == 1
    sdlttf.TTF_SetFontKerning(font, 0)
    assert sdlttf.TTF_GetFontKerning(font) == 0
    sdlttf.TTF_SetFontKerning(font, 1)
    assert sdlttf.TTF_GetFontKerning(font) == 1
    sdlttf.TTF_SetFontKerning(font, 0)
    assert sdlttf.TTF_GetFontKerning(font) == 0

def test_TTF_FontFaces(with_font):
    font = with_font
    assert sdlttf.TTF_FontFaces(font) >= 1

def test_TTF_FontFaceIsFixedWidth(with_font):
    font = with_font
    assert not sdlttf.TTF_FontFaceIsFixedWidth(font)

def test_TTF_FontFaceFamilyName(with_font):
    font = with_font
    assert sdlttf.TTF_FontFaceFamilyName(font) == b"Tuffy"

def test_TTF_FontFaceStyleName(with_font):
    font = with_font
    assert sdlttf.TTF_FontFaceStyleName(font) == b"Regular"

def test_TTF_GlyphIsProvided(with_font):
    font = with_font
    assert isinstance(font.contents, sdlttf.TTF_Font)
    for ch in range(32, 127):
        assert sdlttf.TTF_GlyphIsProvided(font, ch)
    assert not sdlttf.TTF_GlyphIsProvided(font, 0)
    assert not sdlttf.TTF_GlyphIsProvided(font, 0x0ff9)

def test_TTF_GlyphMetrics(with_sdl_ttf):
    expected = {
        'A': [1, 25, 0, 29, 25],
        'j': [-3, 7, -9, 28, 9],
        '.': [2, 7, -1, 4, 8]
    }
    font = sdlttf.TTF_OpenFont(fontfile, 40)
    minX, maxX, minY, maxY = c_int(0), c_int(0), c_int(0), c_int(0)
    adv = c_int(0)
    for char in expected.keys():
        ret = sdlttf.TTF_GlyphMetrics(
            font, ord(char),
            byref(minX), byref(maxX), byref(minY), byref(maxY), byref(adv)
        )
        results = [x.value for x in (minX, maxX, minY, maxY, adv)]
        assert sdlttf.TTF_GetError() == b""
        assert ret == 0
        assert results == expected[char]
    sdlttf.TTF_CloseFont(font)

def test_TTF_SizeText(with_font):
    font = with_font
    min_expected_w = 69     # SDL2_ttf 2.0.18
    max_expected_w = 70     # SDL2_ttf <= 2.0.15
    min_expected_h = 21     # SDL2_ttf 2.0.15 with FreeType 2.10.1
    max_expected_h = 25     # SDL2_ttf < 2.0.15
    w, h = c_int(0), c_int(0)
    sdlttf.TTF_SizeText(font, b"Hi there!", byref(w), byref(h))
    assert w.value >= min_expected_w
    assert w.value <= max_expected_w
    assert h.value >= min_expected_h
    assert h.value <= max_expected_h

def test_TTF_SizeUTF8(with_font):
    font = with_font
    min_expected_w = 72     # SDL2_ttf 2.0.18
    max_expected_w = 73     # SDL2_ttf <= 2.0.15
    min_expected_h = 21     # SDL2_ttf 2.0.15 with FreeType 2.10.1
    max_expected_h = 25     # SDL2_ttf < 2.0.15
    w, h = c_int(0), c_int(0)
    sdlttf.TTF_SizeUTF8(font, u"Hï thère!".encode('utf-8'), byref(w), byref(h))
    assert w.value >= min_expected_w
    assert w.value <= max_expected_w
    assert h.value >= min_expected_h
    assert h.value <= max_expected_h

def test_TTF_SizeUNICODE(with_font):
    font = with_font
    min_expected_w = 69     # SDL2_ttf 2.0.18
    max_expected_w = 70     # SDL2_ttf <= 2.0.15
    min_expected_h = 21     # SDL2_ttf 2.0.15 with FreeType 2.10.1
    max_expected_h = 25     # SDL2_ttf < 2.0.15
    w, h = c_int(0), c_int(0)
    teststr = u"Hi there!"
    strlen = len(teststr) + 1 # +1 for byte-order mark
    intstr = unpack('H' * strlen, teststr.encode('utf-16')) + (0, )
    strarr = (c_uint16 * (strlen + 1))(*intstr)
    sdlttf.TTF_SizeUNICODE(font, strarr, byref(w), byref(h))
    # For debug purposes
    #print(list(strarr))
    #print("w = {0}, h = {1}".format(w.value, h.value))
    assert w.value >= min_expected_w
    assert w.value <= max_expected_w
    assert h.value >= min_expected_h
    assert h.value <= max_expected_h

def test_TTF_Render_Solid(with_font):
    font = with_font
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
    intstr = unpack('H' * strlen, teststr.encode('utf-16')) + (0, )
    strarr = (c_uint16 * (strlen + 1))(*intstr)
    sf = sdlttf.TTF_RenderUNICODE_Solid(font, strarr, color)
    assert isinstance(sf.contents, surface.SDL_Surface)
    # Test TTF_RenderGlyph_Solid
    sf = sdlttf.TTF_RenderGlyph_Solid(font, ord("A"), color)
    assert isinstance(sf.contents, surface.SDL_Surface)

def test_TTF_Render_Shaded(with_font):
    font = with_font
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
    intstr = unpack('H' * strlen, teststr.encode('utf-16')) + (0, )
    strarr = (c_uint16 * (strlen + 1))(*intstr)
    sf = sdlttf.TTF_RenderUNICODE_Shaded(font, strarr, color, bgcolor)
    assert isinstance(sf.contents, surface.SDL_Surface)
    # Test TTF_RenderGlyph_Shaded
    sf = sdlttf.TTF_RenderGlyph_Shaded(font, ord("A"), color, bgcolor)
    assert isinstance(sf.contents, surface.SDL_Surface)

def test_TTF_Render_Blended(with_font):
    font = with_font
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
    intstr = unpack('H' * strlen, teststr.encode('utf-16')) + (0, )
    strarr = (c_uint16 * (strlen + 1))(*intstr)
    sf = sdlttf.TTF_RenderUNICODE_Blended(font, strarr, color)
    assert isinstance(sf.contents, surface.SDL_Surface)
    # Test TTF_RenderGlyph_Blended
    sf = sdlttf.TTF_RenderGlyph_Blended(font, ord("A"), color)
    assert isinstance(sf.contents, surface.SDL_Surface)

def test_TTF_Render_Blended_Wrapped(with_font):
    font = with_font
    color = SDL_Color(0, 0, 0, 255)
    # Test TTF_RenderText_Blended_Wrapped
    teststr = b"Hi there, this is a long line!"
    sf = sdlttf.TTF_RenderText_Blended_Wrapped(font, teststr, color, 100)
    assert isinstance(sf.contents, surface.SDL_Surface)
    assert sf.contents.h > 30
    # Test TTF_RenderUTF8_Blended_Wrapped
    teststr = u"Hï thère, this is a long line!".encode('utf-8')
    sf = sdlttf.TTF_RenderUTF8_Blended_Wrapped(font, teststr, color, 100)
    assert isinstance(sf.contents, surface.SDL_Surface)
    assert sf.contents.h > 30
    # Test TTF_RenderUNICODE_Blended_Wrapped
    # NOTE: no unicode chars because number -> glyph lookup is os-dependent
    teststr = u"Hi there, this is a long line!"
    strlen = len(teststr) + 1 # +1 for byte-order mark
    intstr = unpack('H' * strlen, teststr.encode('utf-16')) + (0, )
    strarr = (c_uint16 * (strlen + 1))(*intstr)
    sf = sdlttf.TTF_RenderUNICODE_Blended_Wrapped(font, strarr, color, 100)
    assert isinstance(sf.contents, surface.SDL_Surface)
    assert sf.contents.h > 30

@pytest.mark.skipif(sdlttf.dll.version < 2014, reason="not available")
def test_TTF_GetFontKerningSizeGlyphs(with_font):
    font = with_font
    # NOTE: Test font (tuffy) has no kerning info, so retval is always 0
    sz = sdlttf.TTF_GetFontKerningSizeGlyphs(font, ord("A"), ord("B"))
    assert sz == 0
