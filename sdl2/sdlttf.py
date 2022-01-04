import os
from ctypes import Structure, POINTER, c_int, c_long, c_char_p, c_void_p
from ctypes import POINTER as _P
from .dll import DLL, SDLFunc
from .version import SDL_version, SDL_VERSIONNUM
from .rwops import SDL_RWops
from .stdinc import Uint16, Uint32
from .pixels import SDL_Color
from .surface import SDL_Surface
from .error import SDL_GetError, SDL_SetError

__all__ = [
    # Opaque Types
    "TTF_Font",

    # Defines
    "SDL_TTF_MAJOR_VERSION", "SDL_TTF_MINOR_VERSION", "SDL_TTF_PATCHLEVEL",
    "TTF_MAJOR_VERSION", "TTF_MINOR_VERSION", "TTF_PATCHLEVEL",
    "UNICODE_BOM_NATIVE", "UNICODE_BOM_SWAPPED",
    "TTF_STYLE_NORMAL", "TTF_STYLE_BOLD", "TTF_STYLE_ITALIC",
    "TTF_STYLE_UNDERLINE", "TTF_STYLE_STRIKETHROUGH",
    "TTF_HINTING_NORMAL", "TTF_HINTING_LIGHT", "TTF_HINTING_MONO",
    "TTF_HINTING_NONE",

    # Macro Functions
    "SDL_TTF_VERSION",  "TTF_VERSION", "SDL_TTF_COMPILEDVERSION",
    "SDL_TTF_VERSION_ATLEAST",

    # Functions
    "TTF_Linked_Version", "TTF_ByteSwappedUNICODE", "TTF_Init",
    "TTF_OpenFont", "TTF_OpenFontIndex", "TTF_OpenFontRW",
    "TTF_OpenFontIndexRW", "TTF_GetFontStyle", "TTF_SetFontStyle",
    "TTF_GetFontOutline", "TTF_SetFontOutline",
    "TTF_GetFontHinting", "TTF_SetFontHinting",
    "TTF_FontHeight", "TTF_FontAscent", "TTF_FontDescent",
    "TTF_FontLineSkip", "TTF_GetFontKerning", "TTF_SetFontKerning",
    "TTF_FontFaces", "TTF_FontFaceIsFixedWidth", "TTF_FontFaceFamilyName",
    "TTF_FontFaceStyleName", "TTF_GlyphIsProvided", "TTF_GlyphMetrics",
    "TTF_SizeText", "TTF_SizeUTF8", "TTF_SizeUNICODE",
    "TTF_RenderText_Solid", "TTF_RenderUTF8_Solid",
    "TTF_RenderUNICODE_Solid", "TTF_RenderGlyph_Solid",
    "TTF_RenderText_Shaded", "TTF_RenderUTF8_Shaded",
    "TTF_RenderUNICODE_Shaded", "TTF_RenderGlyph_Shaded",
    "TTF_RenderText_Blended", "TTF_RenderUTF8_Blended",
    "TTF_RenderUNICODE_Blended", "TTF_RenderText_Blended_Wrapped",
    "TTF_RenderUTF8_Blended_Wrapped", "TTF_RenderUNICODE_Blended_Wrapped",
    "TTF_RenderGlyph_Blended", "TTF_RenderText", "TTF_RenderUTF",
    "TTF_RenderUNICODE", "TTF_CloseFont", "TTF_Quit", "TTF_WasInit",
    "TTF_GetFontKerningSize", "TTF_GetFontKerningSizeGlyphs",
    "TTF_SetError", "TTF_GetError",

    # Python Functions
    "get_dll_file",
]


try:
    dll = DLL("SDL2_ttf", ["SDL2_ttf", "SDL2_ttf-2.0"],
              os.getenv("PYSDL2_DLL_PATH"))
except RuntimeError as exc:
    raise ImportError(exc)

def get_dll_file():
    """Gets the file name of the loaded SDL2_ttf library."""
    return dll.libfile

_bind = dll.bind_function


# Constants, enums, type definitions, and macros

SDL_TTF_MAJOR_VERSION = 2
SDL_TTF_MINOR_VERSION = 0
SDL_TTF_PATCHLEVEL = 15

def SDL_TTF_VERSION(x):
    x.major = SDL_TTF_MAJOR_VERSION
    x.minor = SDL_TTF_MINOR_VERSION
    x.patch = SDL_TTF_PATCHLEVEL

TTF_MAJOR_VERSION = SDL_TTF_MAJOR_VERSION
TTF_MINOR_VERSION = SDL_TTF_MINOR_VERSION
TTF_PATCHLEVEL = SDL_TTF_PATCHLEVEL
TTF_VERSION = SDL_TTF_VERSION

SDL_TTF_COMPILEDVERSION = SDL_VERSIONNUM(SDL_TTF_MAJOR_VERSION, SDL_TTF_MINOR_VERSION, SDL_TTF_PATCHLEVEL)
SDL_TTF_VERSION_ATLEAST = lambda x, y, z: (SDL_TTF_COMPILEDVERSION >= SDL_VERSIONNUM(x, y, z))

UNICODE_BOM_NATIVE = 0xFEFF
UNICODE_BOM_SWAPPED = 0xFFFE

TTF_STYLE_NORMAL = 0x00
TTF_STYLE_BOLD = 0x01
TTF_STYLE_ITALIC = 0x02
TTF_STYLE_UNDERLINE = 0x04
TTF_STYLE_STRIKETHROUGH = 0x08

TTF_HINTING_NORMAL = 0
TTF_HINTING_LIGHT = 1
TTF_HINTING_MONO = 2
TTF_HINTING_NONE = 3

class TTF_Font(c_void_p):
    pass


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("TTF_Linked_Version", None, _P(SDL_version)),
    SDLFunc("TTF_ByteSwappedUNICODE", [c_int], None),
    SDLFunc("TTF_Init", None, c_int),
    SDLFunc("TTF_OpenFont", [c_char_p, c_int], _P(TTF_Font)),
    SDLFunc("TTF_OpenFontIndex", [c_char_p, c_int, c_long], _P(TTF_Font)),
    SDLFunc("TTF_OpenFontRW", [_P(SDL_RWops), c_int, c_int], _P(TTF_Font)),
    SDLFunc("TTF_OpenFontIndexRW", [_P(SDL_RWops), c_int, c_int, c_long], _P(TTF_Font)),
    SDLFunc("TTF_GetFontStyle", [_P(TTF_Font)], c_int),
    SDLFunc("TTF_SetFontStyle", [_P(TTF_Font), c_int], None),
    SDLFunc("TTF_GetFontOutline", [_P(TTF_Font)], c_int),
    SDLFunc("TTF_SetFontOutline", [_P(TTF_Font), c_int], None),
    SDLFunc("TTF_GetFontHinting", [_P(TTF_Font)], c_int),
    SDLFunc("TTF_SetFontHinting", [_P(TTF_Font), c_int], None),
    SDLFunc("TTF_FontHeight", [_P(TTF_Font)], c_int),
    SDLFunc("TTF_FontAscent", [_P(TTF_Font)], c_int),
    SDLFunc("TTF_FontDescent", [_P(TTF_Font)], c_int),
    SDLFunc("TTF_FontLineSkip", [_P(TTF_Font)], c_int),
    SDLFunc("TTF_GetFontKerning", [_P(TTF_Font)], c_int),
    SDLFunc("TTF_SetFontKerning", [_P(TTF_Font), c_int]),
    SDLFunc("TTF_FontFaces", [_P(TTF_Font)], c_long),
    SDLFunc("TTF_FontFaceIsFixedWidth", [_P(TTF_Font)], c_int),
    SDLFunc("TTF_FontFaceFamilyName", [_P(TTF_Font)], c_char_p),
    SDLFunc("TTF_FontFaceStyleName", [_P(TTF_Font)], c_char_p),
    SDLFunc("TTF_GlyphIsProvided", [_P(TTF_Font), Uint16], c_int),
    SDLFunc("TTF_GlyphMetrics", [_P(TTF_Font), Uint16, _P(c_int), _P(c_int), _P(c_int), _P(c_int), _P(c_int)], c_int),
    SDLFunc("TTF_SizeText", [_P(TTF_Font), c_char_p, _P(c_int), _P(c_int)], c_int),
    SDLFunc("TTF_SizeUTF8", [_P(TTF_Font), c_char_p, _P(c_int), _P(c_int)], c_int),
    SDLFunc("TTF_SizeUNICODE", [_P(TTF_Font), _P(Uint16), _P(c_int), _P(c_int)], c_int),
    SDLFunc("TTF_RenderText_Solid", [_P(TTF_Font), c_char_p, SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderUTF8_Solid", [_P(TTF_Font), c_char_p, SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderUNICODE_Solid", [_P(TTF_Font), _P(Uint16), SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderGlyph_Solid", [_P(TTF_Font), Uint16, SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderText_Shaded", [_P(TTF_Font), c_char_p, SDL_Color, SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderUTF8_Shaded", [_P(TTF_Font), c_char_p, SDL_Color, SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderUNICODE_Shaded", [_P(TTF_Font), _P(Uint16), SDL_Color, SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderGlyph_Shaded", [_P(TTF_Font), Uint16, SDL_Color, SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderText_Blended", [_P(TTF_Font), c_char_p, SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderUTF8_Blended", [_P(TTF_Font), c_char_p, SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderUNICODE_Blended", [_P(TTF_Font), _P(Uint16), SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_RenderText_Blended_Wrapped", [_P(TTF_Font), c_char_p, SDL_Color, Uint32], _P(SDL_Surface)),
    SDLFunc("TTF_RenderUTF8_Blended_Wrapped", [_P(TTF_Font), c_char_p, SDL_Color, Uint32], _P(SDL_Surface)),
    SDLFunc("TTF_RenderUNICODE_Blended_Wrapped", [_P(TTF_Font), _P(Uint16), SDL_Color, Uint32], _P(SDL_Surface)),
    SDLFunc("TTF_RenderGlyph_Blended", [_P(TTF_Font), Uint16, SDL_Color], _P(SDL_Surface)),
    SDLFunc("TTF_CloseFont", [_P(TTF_Font)]),
    SDLFunc("TTF_Quit"),
    SDLFunc("TTF_WasInit", None, c_int),
    SDLFunc("TTF_GetFontKerningSize", [_P(TTF_Font), c_int, c_int], c_int),
    SDLFunc("TTF_GetFontKerningSizeGlyphs", [_P(TTF_Font), Uint16, Uint16], c_int, added='2.0.14'),
]
_funcs = {}
for f in _funcdefs:
    _funcs[f.name] = _bind(f.name, f.args, f.returns, f.added)


# Python wrapper functions

def TTF_Linked_Version():
    return _funcs["TTF_Linked_Version"]()

def TTF_ByteSwappedUNICODE(swapped):
    return _funcs["TTF_ByteSwappedUNICODE"](swapped)

def TTF_Init():
    return _funcs["TTF_Init"]()


def TTF_OpenFont(file, ptsize):
    return _funcs["TTF_OpenFont"](file, ptsize)

def TTF_OpenFontIndex(file, ptsize, index):
    return _funcs["TTF_OpenFontIndex"](file, ptsize, index)

def TTF_OpenFontRW(src, freesrc, ptsize):
    return _funcs["TTF_OpenFontRW"](src, freesrc, ptsize)

def TTF_OpenFontIndexRW(src, freesrc, ptsize, index):
    return _funcs["TTF_OpenFontIndexRW"](src, freesrc, ptsize, index)


def TTF_GetFontStyle(font):
    return _funcs["TTF_GetFontStyle"](font)

def TTF_SetFontStyle(font, style):
    return _funcs["TTF_SetFontStyle"](font, style)

def TTF_GetFontOutline(font):
    return _funcs["TTF_GetFontOutline"](font)

def TTF_SetFontOutline(font, outline):
    return _funcs["TTF_SetFontOutline"](font, outline)

def TTF_GetFontHinting(font):
    return _funcs["TTF_GetFontHinting"](font)

def TTF_SetFontHinting(font, hinting):
    return _funcs["TTF_SetFontHinting"](font, hinting)


def TTF_FontHeight(font):
    return _funcs["TTF_FontHeight"](font)

def TTF_FontAscent(font):
    return _funcs["TTF_FontAscent"](font)

def TTF_FontDescent(font):
    return _funcs["TTF_FontDescent"](font)

def TTF_FontLineSkip(font):
    return _funcs["TTF_FontLineSkip"](font)

def TTF_GetFontKerning(font):
    return _funcs["TTF_GetFontKerning"](font)

def TTF_SetFontKerning(font, allowed):
    return _funcs["TTF_SetFontKerning"](font, allowed)

def TTF_FontFaces(font):
    return _funcs["TTF_FontFaces"](font)

def TTF_FontFaceIsFixedWidth(font):
    return _funcs["TTF_FontFaceIsFixedWidth"](font)

def TTF_FontFaceFamilyName(font):
    return _funcs["TTF_FontFaceFamilyName"](font)

def TTF_FontFaceStyleName(font):
    return _funcs["TTF_FontFaceStyleName"](font)

def TTF_GlyphIsProvided(font, ch):
    return _funcs["TTF_GlyphIsProvided"](font, ch)

def TTF_GlyphMetrics(font, ch, minx, maxx, miny, maxy, advance):
    return _funcs["TTF_GlyphMetrics"](font, ch, minx, maxx, miny, maxy, advance)


def TTF_SizeText(font, text, w, h):
    return _funcs["TTF_SizeText"](font, text, w, h)

def TTF_SizeUTF8(font, text, w, h):
    return _funcs["TTF_SizeUTF8"](font, text, w, h)

def TTF_SizeUNICODE(font, text, w, h):
    return _funcs["TTF_SizeUNICODE"](font, text, w, h)


def TTF_RenderText_Solid(font, text, fg):
    return _funcs["TTF_RenderText_Solid"](font, text, fg)

def TTF_RenderUTF8_Solid(font, text, fg):
    return _funcs["TTF_RenderUTF8_Solid"](font, text, fg)

def TTF_RenderUNICODE_Solid(font, text, fg):
    return _funcs["TTF_RenderUNICODE_Solid"](font, text, fg)

def TTF_RenderGlyph_Solid(font, ch, fg):
    return _funcs["TTF_RenderGlyph_Solid"](font, ch, fg)

def TTF_RenderText_Shaded(font, text, fg, bg):
    return _funcs["TTF_RenderText_Shaded"](font, text, fg, bg)

def TTF_RenderUTF8_Shaded(font, text, fg, bg):
    return _funcs["TTF_RenderUTF8_Shaded"](font, text, fg, bg)

def TTF_RenderUNICODE_Shaded(font, text, fg, bg):
    return _funcs["TTF_RenderUNICODE_Shaded"](font, text, fg, bg)

def TTF_RenderGlyph_Shaded(font, ch, fg, bg):
    return _funcs["TTF_RenderGlyph_Shaded"](font, ch, fg, bg)

def TTF_RenderText_Blended(font, text, fg):
    return _funcs["TTF_RenderText_Blended"](font, text, fg)

def TTF_RenderUTF8_Blended(font, text, fg):
    return _funcs["TTF_RenderUTF8_Blended"](font, text, fg)

def TTF_RenderUNICODE_Blended(font, text, fg):
    return _funcs["TTF_RenderUNICODE_Blended"](font, text, fg)

def TTF_RenderText_Blended_Wrapped(font, text, fg, wrapLength):
    return _funcs["TTF_RenderText_Blended_Wrapped"](font, text, fg, wrapLength)

def TTF_RenderUTF8_Blended_Wrapped(font, text, fg, wrapLength):
    return _funcs["TTF_RenderUTF8_Blended_Wrapped"](font, text, fg, wrapLength)

def TTF_RenderUNICODE_Blended_Wrapped(font, text, fg, wrapLength):
    return _funcs["TTF_RenderUNICODE_Blended_Wrapped"](font, text, fg, wrapLength)

def TTF_RenderGlyph_Blended(font, ch, fg):
    return _funcs["TTF_RenderGlyph_Blended"](font, ch, fg)

TTF_RenderText = TTF_RenderText_Shaded
TTF_RenderUTF8 = TTF_RenderUTF8_Shaded
TTF_RenderUNICODE = TTF_RenderUNICODE_Shaded


def TTF_CloseFont(font):
    return _funcs["TTF_CloseFont"](font)

def TTF_Quit():
    return _funcs["TTF_Quit"]()

def TTF_WasInit():
    return _funcs["TTF_WasInit"]()

def TTF_GetFontKerningSize(font, prev_index, index):
    return _funcs["TTF_GetFontKerningSize"](font, prev_index, index)

def TTF_GetFontKerningSizeGlyphs(font, previous_ch, ch):
    return _funcs["TTF_GetFontKerningSizeGlyphs"](font, previous_ch, ch)

TTF_SetError = SDL_SetError
TTF_GetError = SDL_GetError
