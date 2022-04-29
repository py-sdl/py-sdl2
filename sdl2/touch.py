from ctypes import Structure, c_float, c_int
from ctypes import POINTER as _P
from .dll import _bind, SDLFunc, AttributeDict
from .stdinc import Sint64

__all__ = [
    # Structs
    "SDL_Finger",

    # Defines
    "SDL_TouchID", "SDL_FingerID", 
    "SDL_TOUCH_MOUSEID", "SDL_MOUSE_TOUCHID",

    # Enums
    "SDL_TouchDeviceType",
    "SDL_TOUCH_DEVICE_INVALID", "SDL_TOUCH_DEVICE_DIRECT",
    "SDL_TOUCH_DEVICE_INDIRECT_ABSOLUTE",
    "SDL_TOUCH_DEVICE_INDIRECT_RELATIVE",

    # Functions
    "SDL_GetNumTouchDevices", "SDL_GetTouchDevice",
    "SDL_GetTouchDeviceType", "SDL_GetNumTouchFingers",
    "SDL_GetTouchFinger"
]


# Constants & enums

SDL_TouchDeviceType = c_int
SDL_TOUCH_DEVICE_INVALID = -1,
SDL_TOUCH_DEVICE_DIRECT = 0
SDL_TOUCH_DEVICE_INDIRECT_ABSOLUTE = 1
SDL_TOUCH_DEVICE_INDIRECT_RELATIVE = 2

SDL_TOUCH_MOUSEID = 2**32 - 1 # defined as ((Uint32)-1), hope this is right
SDL_MOUSE_TOUCHID = 2**63 - 1 # defined as ((Sint64)-1), hope this is right


# Struct definitions & typedefs

SDL_TouchID = Sint64
SDL_FingerID = Sint64

class SDL_Finger(Structure):
    _fields_ = [
        ("id", SDL_FingerID),
        ("x", c_float),
        ("y", c_float),
        ("pressure", c_float),
    ]


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("SDL_GetNumTouchDevices", None, c_int),
    SDLFunc("SDL_GetTouchDevice", [c_int], SDL_TouchID),
    SDLFunc("SDL_GetTouchDeviceType", [SDL_TouchID], SDL_TouchDeviceType, added='2.0.10'),
    SDLFunc("SDL_GetNumTouchFingers", [SDL_TouchID], c_int),
    SDLFunc("SDL_GetTouchFinger", [SDL_TouchID, c_int], _P(SDL_Finger)),
]
_ctypes = AttributeDict()
for f in _funcdefs:
    _ctypes[f.name] = _bind(f.name, f.args, f.returns, f.added)


# Aliases for ctypes bindings

SDL_GetNumTouchDevices = _ctypes["SDL_GetNumTouchDevices"]
SDL_GetTouchDevice = _ctypes["SDL_GetTouchDevice"]
SDL_GetTouchDeviceType = _ctypes["SDL_GetTouchDeviceType"]
SDL_GetNumTouchFingers = _ctypes["SDL_GetNumTouchFingers"]
SDL_GetTouchFinger = _ctypes["SDL_GetTouchFinger"]
