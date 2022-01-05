import os
from ctypes import Structure, POINTER, c_int, c_float, c_void_p, c_char, \
    c_char_p, c_double
from ctypes import POINTER as _P
from .dll import DLL, SDLFunc
from .stdinc import Uint8, Uint32, Sint16
from .render import SDL_Renderer
from .surface import SDL_Surface

# NOTE: This module is currently missing wrappers for the image filtering
# functions in SDL2_imageFilter.h. However, because we have Pillow on Python
# this isn't really a pressing concern. Time permitting, these functions may
# be wrapped at a later date for the sake of completeness.

__all__ = [
    # Structs
    "FPSManager",
    
    # Defines
    "FPS_UPPER_LIMIT", "FPS_LOWER_LIMIT", "FPS_DEFAULT",
    "SDL2_GFXPRIMITIVES_MAJOR", "SDL2_GFXPRIMITIVES_MAJOR",
    "SDL2_GFXPRIMITIVES_MICRO", "SMOOTHING_OFF", "SMOOTHING_ON",

    # Functions
    "SDL_initFramerate", "SDL_getFramerate",
    "SDL_setFramerate", "SDL_getFramecount", "SDL_framerateDelay",
    "pixelColor", "pixelRGBA", "hlineColor",
    "hlineRGBA", "vlineColor", "vlineRGBA", "rectangleColor",
    "rectangleRGBA", "roundedRectangleColor", "roundedRectangleRGBA",
    "boxColor", "boxRGBA", "roundedBoxColor", "roundedBoxRGBA",
    "lineColor", "lineRGBA", "aalineColor", "aalineRGBA",
    "thickLineColor", "thickLineRGBA", "circleColor", "circleRGBA",
    "arcColor", "arcRGBA", "aacircleColor", "aacircleRGBA",
    "filledCircleColor", "filledCircleRGBA", "ellipseColor",
    "ellipseRGBA", "aaellipseColor", "aaellipseRGBA",
    "filledEllipseColor", "filledEllipseRGBA", "pieColor", "pieRGBA",
    "filledPieColor", "filledPieRGBA", "trigonColor", "trigonRGBA",
    "aatrigonColor", "aatrigonRGBA", "filledTrigonColor",
    "filledTrigonRGBA", "polygonColor", "polygonRGBA", "aapolygonColor",
    "aapolygonRGBA", "filledPolygonColor", "filledPolygonRGBA",
    "texturedPolygon", "bezierColor", "bezierRGBA",
    "gfxPrimitivesSetFont", "gfxPrimitivesSetFontRotation",
    "characterColor", "characterRGBA", "stringColor", "stringRGBA",
    "rotozoomSurface", "rotozoomSurfaceXY", "rotozoomSurfaceSize",
    "rotozoomSurfaceSizeXY", "zoomSurface", "zoomSurfaceSize", "shrinkSurface",
    "rotateSurface90Degrees",

    # Python Functions
    "get_dll_file"
]


try:
    dll = DLL("SDL2_gfx", ["SDL2_gfx", "SDL2_gfx-1.0"],
              os.getenv("PYSDL2_DLL_PATH"))
except RuntimeError as exc:
    raise ImportError(exc)


def get_dll_file():
    """Gets the file name of the loaded SDL2_gfx library."""
    return dll.libfile

_bind = dll.bind_function


# Constants, enums, type definitions, and macros

SDL2_GFXPRIMITIVES_MAJOR = 1
SDL2_GFXPRIMITIVES_MINOR = 0
SDL2_GFXPRIMITIVES_MICRO = 4

FPS_UPPER_LIMIT = 200
FPS_LOWER_LIMIT = 1
FPS_DEFAULT = 30

SMOOTHING_OFF = 0
SMOOTHING_ON = 1

class FPSManager(Structure):
    _fields_ = [("framecount", Uint32),
                ("rateticks", c_float),
                ("baseticks", Uint32),
                ("lastticks", Uint32),
                ("rate", Uint32)
                ]


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("SDL_initFramerate", [_P(FPSManager)]),
    SDLFunc("SDL_setFramerate", [_P(FPSManager), Uint32], c_int),
    SDLFunc("SDL_getFramerate", [_P(FPSManager)], c_int),
    SDLFunc("SDL_getFramecount", [_P(FPSManager)], Uint32),
    SDLFunc("SDL_framerateDelay", [_P(FPSManager)], Uint32),
    SDLFunc("pixelColor", [_P(SDL_Renderer), Sint16, Sint16, Uint32], c_int),
    SDLFunc("pixelRGBA", [_P(SDL_Renderer), Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("hlineColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("hlineRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("vlineColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("vlineRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("rectangleColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("rectangleRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("roundedRectangleColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("roundedRectangleRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("boxColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("boxRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("roundedBoxColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("roundedBoxRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("lineColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("lineRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("aalineColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("aalineRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("thickLineColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint32], c_int),
    SDLFunc("thickLineRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("circleColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("circleRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("arcColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("arcRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("aacircleColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("aacircleRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("filledCircleColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("filledCircleRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("ellipseColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("ellipseRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("aaellipseColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("aaellipseRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("filledEllipseColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("filledEllipseRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("pieColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("pieRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("filledPieColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("filledPieRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("trigonColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("trigonRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("aatrigonColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("aatrigonRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("filledTrigonColor", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint32], c_int),
    SDLFunc("filledTrigonRGBA", [_P(SDL_Renderer), Sint16, Sint16, Sint16, Sint16, Sint16, Sint16, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("polygonColor", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, Uint32], c_int),
    SDLFunc("polygonRGBA", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("aapolygonColor", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, Uint32], c_int),
    SDLFunc("aapolygonRGBA", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("filledPolygonColor", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, Uint32], c_int),
    SDLFunc("filledPolygonRGBA", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("texturedPolygon", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, _P(SDL_Surface), c_int, c_int], c_int),
    SDLFunc("bezierColor", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, c_int, Uint32], c_int),
    SDLFunc("bezierRGBA", [_P(SDL_Renderer), _P(Sint16), _P(Sint16), c_int, c_int, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("gfxPrimitivesSetFont", [c_void_p, Uint32, Uint32]),
    SDLFunc("gfxPrimitivesSetFontRotation", [Uint32]),
    SDLFunc("characterColor", [_P(SDL_Renderer), Sint16, Sint16, c_char, Uint32], c_int),
    SDLFunc("characterRGBA", [_P(SDL_Renderer), Sint16, Sint16, c_char, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("stringColor", [_P(SDL_Renderer), Sint16, Sint16, c_char_p, Uint32], c_int),
    SDLFunc("stringRGBA", [_P(SDL_Renderer), Sint16, Sint16, c_char_p, Uint8, Uint8, Uint8, Uint8], c_int),
    SDLFunc("rotozoomSurface", [_P(SDL_Surface), c_double, c_double, c_int], _P(SDL_Surface)),
    SDLFunc("rotozoomSurfaceXY", [_P(SDL_Surface), c_double, c_double, c_double, c_int], _P(SDL_Surface)),
    SDLFunc("rotozoomSurfaceSize", [c_int, c_int, c_double, c_double, _P(c_int), _P(c_int)]),
    SDLFunc("rotozoomSurfaceSizeXY", [c_int, c_int, c_double, c_double, c_double, _P(c_int), _P(c_int)]),
    SDLFunc("zoomSurface", [_P(SDL_Surface), c_double, c_double, c_int], _P(SDL_Surface)),
    SDLFunc("zoomSurfaceSize", [c_int, c_int, c_double, c_double, _P(c_int), _P(c_int)]),
    SDLFunc("shrinkSurface", [_P(SDL_Surface), c_int, c_int], _P(SDL_Surface)),
    SDLFunc("rotateSurface90Degrees", [_P(SDL_Surface), c_int], _P(SDL_Surface)),
]
_funcs = {}
for f in _funcdefs:
    _funcs[f.name] = _bind(f.name, f.args, f.returns, f.added)


# Python wrapper functions

def SDL_initFramerate(manager):
    return _funcs["SDL_initFramerate"](manager)

def SDL_setFramerate(manager, rate):
    return _funcs["SDL_setFramerate"](manager, rate)

def SDL_getFramerate(manager):
    return _funcs["SDL_getFramerate"](manager)

def SDL_getFramecount(manager):
    return _funcs["SDL_getFramecount"](manager)

def SDL_framerateDelay(manager):
    return _funcs["SDL_framerateDelay"](manager)


def pixelColor(renderer, x, y, color):
    return _funcs["pixelColor"](renderer, x, y, color)

def pixelRGBA(renderer, x, y, r, g, b, a):
    return _funcs["pixelRGBA"](renderer, x, y, r, g, b, a)

def hlineColor(renderer, x1, x2, y, color):
    return _funcs["hlineColor"](renderer, x1, x2, y, color)

def hlineRGBA(renderer, x1, x2, y, r, g, b, a):
    return _funcs["hlineRGBA"](renderer, x1, x2, y, r, g, b, a)

def vlineColor(renderer, x, y1, y2, color):
    return _funcs["vlineColor"](renderer, x, y1, y2, color)

def vlineRGBA(renderer, x, y1, y2, r, g, b, a):
    return _funcs["vlineRGBA"](renderer, x, y1, y2, r, g, b, a)


def rectangleColor(renderer, x1, y1, x2, y2, color):
    return _funcs["rectangleColor"](renderer, x1, y1, x2, y2, color)

def rectangleRGBA(renderer, x1, y1, x2, y2, r, g, b, a):
    return _funcs["rectangleRGBA"](renderer, x1, y1, x2, y2, r, g, b, a)

def roundedRectangleColor(renderer, x1, y1, x2, y2, rad, color):
    return _funcs["roundedRectangleColor"](renderer, x1, y1, x2, y2, rad, color)

def roundedRectangleRGBA(renderer, x1, y1, x2, y2, rad, r, g, b, a):
    return _funcs["roundedRectangleRGBA"](renderer, x1, y1, x2, y2, rad, r, g, b, a)

def boxColor(renderer, x1, y1, x2, y2, color):
    return _funcs["boxColor"](renderer, x1, y1, x2, y2, color)

def boxRGBA(renderer, x1, y1, x2, y2, r, g, b, a):
    return _funcs["boxRGBA"](renderer, x1, y1, x2, y2, r, g, b, a)

def roundedBoxColor(renderer, x1, y1, x2, y2, rad, color):
    return _funcs["roundedBoxColor"](renderer, x1, y1, x2, y2, rad, color)

def roundedBoxRGBA(renderer, x1, y1, x2, y2, rad, r, g, b, a):
    return _funcs["roundedBoxRGBA"](renderer, x1, y1, x2, y2, rad, r, g, b, a)


def lineColor(renderer, x1, y1, x2, y2, color):
    return _funcs["lineColor"](renderer, x1, y1, x2, y2, color)

def lineRGBA(renderer, x1, y1, x2, y2, r, g, b, a):
    return _funcs["lineRGBA"](renderer, x1, y1, x2, y2, r, g, b, a)

def aalineColor(renderer, x1, y1, x2, y2, color):
    return _funcs["aalineColor"](renderer, x1, y1, x2, y2, color)

def aalineRGBA(renderer, x1, y1, x2, y2, r, g, b, a):
    return _funcs["aalineRGBA"](renderer, x1, y1, x2, y2, r, g, b, a)

def thickLineColor(renderer, x1, y1, x2, y2, width, color):
    return _funcs["thickLineColor"](renderer, x1, y1, x2, y2, width, color)

def thickLineRGBA(renderer, x1, y1, x2, y2, width, r, g, b, a):
    return _funcs["thickLineRGBA"](renderer, x1, y1, x2, y2, width, r, g, b, a)


def circleColor(renderer, x, y, rad, color):
    return _funcs["circleColor"](renderer, x, y, rad, color)

def circleRGBA(renderer, x, y, rad, r, g, b, a):
    return _funcs["circleRGBA"](renderer, x, y, rad, r, g, b, a)

def arcColor(renderer, x, y, rad, start, end, color):
    return _funcs["arcColor"](renderer, x, y, rad, start, end, color)

def arcRGBA(renderer, x, y, rad, start, end, r, g, b, a):
    return _funcs["arcRGBA"](renderer, x, y, rad, start, end, r, g, b, a)

def aacircleColor(renderer, x, y, rad, color):
    return _funcs["aacircleColor"](renderer, x, y, rad, color)

def aacircleRGBA(renderer, x, y, rad, r, g, b, a):
    return _funcs["aacircleRGBA"](renderer, x, y, rad, r, g, b, a)

def filledCircleColor(renderer, x, y, rad, color):
    return _funcs["filledCircleColor"](renderer, x, y, rad, color)

def filledCircleRGBA(renderer, x, y, rad, r, g, b, a):
    return _funcs["filledCircleRGBA"](renderer, x, y, rad, r, g, b, a)


def ellipseColor(renderer, x, y, rx, ry, color):
    return _funcs["ellipseColor"](renderer, x, y, rx, ry, color)

def ellipseRGBA(renderer, x, y, rx, ry, r, g, b, a):
    return _funcs["ellipseRGBA"](renderer, x, y, rx, ry, r, g, b, a)

def aaellipseColor(renderer, x, y, rx, ry, color):
    return _funcs["aaellipseColor"](renderer, x, y, rx, ry, color)

def aaellipseRGBA(renderer, x, y, rx, ry, r, g, b, a):
    return _funcs["aaellipseRGBA"](renderer, x, y, rx, ry, r, g, b, a)

def filledEllipseColor(renderer, x, y, rx, ry, color):
    return _funcs["filledEllipseColor"](renderer, x, y, rx, ry, color)

def filledEllipseRGBA(renderer, x, y, rx, ry, r, g, b, a):
    return _funcs["filledEllipseRGBA"](renderer, x, y, rx, ry, r, g, b, a)


def pieColor(renderer, x, y, rad, start, end, color):
    return _funcs["pieColor"](renderer, x, y, rad, start, end, color)

def pieRGBA(renderer, x, y, rad, start, end, r, g, b, a):
    return _funcs["pieRGBA"](renderer, x, y, rad, start, end, r, g, b, a)

def filledPieColor(renderer, x, y, rad, start, end, color):
    return _funcs["filledPieColor"](renderer, x, y, rad, start, end, color)

def filledPieRGBA(renderer, x, y, rad, start, end, r, g, b, a):
    return _funcs["filledPieRGBA"](renderer, x, y, rad, start, end, r, g, b, a)


def trigonColor(renderer, x1, y1, x2, y2, x3, y3, color):
    return _funcs["trigonColor"](renderer, x1, y1, x2, y2, x3, y3, color)

def trigonRGBA(renderer, x1, y1, x2, y2, x3, y3, r, g, b, a):
    return _funcs["trigonRGBA"](renderer, x1, y1, x2, y2, x3, y3, r, g, b, a)

def aatrigonColor(renderer, x1, y1, x2, y2, x3, y3, color):
    return _funcs["aatrigonColor"](renderer, x1, y1, x2, y2, x3, y3, color)

def aatrigonRGBA(renderer, x1, y1, x2, y2, x3, y3, r, g, b, a):
    return _funcs["aatrigonRGBA"](renderer, x1, y1, x2, y2, x3, y3, r, g, b, a)

def filledTrigonColor(renderer, x1, y1, x2, y2, x3, y3, color):
    return _funcs["filledTrigonColor"](renderer, x1, y1, x2, y2, x3, y3, color)

def filledTrigonRGBA(renderer, x1, y1, x2, y2, x3, y3, r, g, b, a):
    return _funcs["filledTrigonRGBA"](renderer, x1, y1, x2, y2, x3, y3, r, g, b, a)


def polygonColor(renderer, vx, vy, n, color):
    return _funcs["polygonColor"](renderer, vx, vy, n, color)

def polygonRGBA(renderer, vx, vy, n, r, g, b, a):
    return _funcs["polygonRGBA"](renderer, vx, vy, n, r, g, b, a)

def aapolygonColor(renderer, vx, vy, n, color):
    return _funcs["aapolygonColor"](renderer, vx, vy, n, color)

def aapolygonRGBA(renderer, vx, vy, n, r, g, b, a):
    return _funcs["aapolygonRGBA"](renderer, vx, vy, n, r, g, b, a)

def filledPolygonColor(renderer, vx, vy, n, color):
    return _funcs["filledPolygonColor"](renderer, vx, vy, n, color)

def filledPolygonRGBA(renderer, vx, vy, n, r, g, b, a):
    return _funcs["filledPolygonRGBA"](renderer, vx, vy, n, r, g, b, a)

def texturedPolygon(renderer, vx, vy, n, texture, texture_dx, texture_dy):
    return _funcs["texturedPolygon"](
        renderer, vx, vy, n, texture, texture_dx, texture_dy
    )


def bezierColor(renderer, vx, vy, n, s, color):
    return _funcs["bezierColor"](renderer, vx, vy, n, s, color)

def bezierRGBA(renderer, vx, vy, n, s, r, g, b, a):
    return _funcs["bezierRGBA"](renderer, vx, vy, n, s, r, g, b, a)


def gfxPrimitivesSetFont(fontdata, cw, ch):
    return _funcs["gfxPrimitivesSetFont"](fontdata, cw, ch)

def gfxPrimitivesSetFontRotation(rotation):
    return _funcs["gfxPrimitivesSetFontRotation"](rotation)

def characterColor(renderer, x, y, c, color):
    return _funcs["characterColor"](renderer, x, y, c, color)

def characterRGBA(renderer, x, y, c, r, g, b, a):
    return _funcs["characterRGBA"](renderer, x, y, c, r, g, b, a)

def stringColor(renderer, x, y, s, color):
    return _funcs["stringColor"](renderer, x, y, s, color)

def stringRGBA(renderer, x, y, s, r, g, b, a):
    return _funcs["stringRGBA"](renderer, x, y, s, r, g, b, a)


def rotozoomSurface(src, angle, zoom, smooth):
    return _funcs["rotozoomSurface"](src, angle, zoom, smooth)

def rotozoomSurfaceXY(src, angle, zoomx, zoomy, smooth):
    return _funcs["rotozoomSurfaceXY"](src, angle, zoomx, zoomy, smooth)

def rotozoomSurfaceSize(width, height, angle, zoom, dstwidth, dstheight):
    return _funcs["rotozoomSurfaceSize"](
        width, height, angle, zoom, dstwidth, dstheight
    )

def rotozoomSurfaceSizeXY(width, height, angle, zoomx, zoomy, dstwidth, dstheight):
    return _funcs["rotozoomSurfaceSizeXY"](
        width, height, angle, zoomx, zoomy, dstwidth, dstheight
    )

def zoomSurface(src, zoomx, zoomy, smooth):
    return _funcs["zoomSurface"](src, zoomx, zoomy, smooth)

def zoomSurfaceSize(width, height, zoomx, zoomy, dstwidth, dstheight):
    return _funcs["zoomSurfaceSize"](width, height, zoomx, zoomy, dstwidth, dstheight)

def shrinkSurface(src, factorx, factory):
    return _funcs["shrinkSurface"](src, factorx, factory)

def rotateSurface90Degrees(src, numClockwiseTurns):
    return _funcs["rotateSurface90Degrees"](src, numClockwiseTurns)
