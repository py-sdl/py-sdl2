from ctypes import Union, Structure, c_char_p, c_uint, c_int
from ctypes import POINTER as _P
from .dll import _bind
from .stdinc import Uint8, Uint32, SDL_bool
from .pixels import SDL_Color
from .surface import SDL_Surface
from .video import SDL_Window

__all__ = [
    # Structs & Unions
    "SDL_WindowShapeParams", "SDL_WindowShapeMode",

    # Defines
    "SDL_NONSHAPEABLE_WINDOW", "SDL_INVALID_SHAPE_ARGUMENT",
    "SDL_WINDOW_LACKS_SHAPE",

    # Enums
    "WindowShapeMode",
    "ShapeModeDefault", "ShapeModeBinarizeAlpha",
    "ShapeModeReverseBinarizeAlpha", "ShapeModeColorKey",

    # Macro Functions
    "SDL_SHAPEMODEALPHA",

    # Functions
    "SDL_CreateShapedWindow", "SDL_IsShapedWindow", "SDL_SetWindowShape",
    "SDL_GetShapedWindowMode"
]


# Constants & enums

SDL_NONSHAPEABLE_WINDOW = -1
SDL_INVALID_SHAPE_ARGUMENT = -2
SDL_WINDOW_LACKS_SHAPE = -3

WindowShapeMode = c_int
ShapeModeDefault = 0
ShapeModeBinarizeAlpha = 1
ShapeModeReverseBinarizeAlpha = 2
ShapeModeColorKey = 3


# Macros & inline functions

SDL_SHAPEMODEALPHA = lambda mode: (mode == ShapeModeDefault or mode == ShapeModeBinarizeAlpha or mode == ShapeModeReverseBinarizeAlpha)


# Struct definitions

class SDL_WindowShapeParams(Union):
    _fields_ = [
        ("binarizationCutoff", Uint8),
        ("colorKey", SDL_Color),
    ]

class SDL_WindowShapeMode(Structure):
    _fields_ = [
        ("mode", WindowShapeMode),
        ("parameters", SDL_WindowShapeParams),
    ]



SDL_CreateShapedWindow = _bind("SDL_CreateShapedWindow", [c_char_p, c_uint, c_uint, c_uint, c_uint, Uint32], _P(SDL_Window))
SDL_IsShapedWindow = _bind("SDL_IsShapedWindow", [_P(SDL_Window)], SDL_bool)
SDL_SetWindowShape = _bind("SDL_SetWindowShape", [_P(SDL_Window), _P(SDL_Surface), _P(SDL_WindowShapeMode)], c_int)
SDL_GetShapedWindowMode = _bind("SDL_GetShapedWindowMode", [_P(SDL_Window), _P(SDL_WindowShapeMode)], c_int)
