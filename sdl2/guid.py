from ctypes import Structure, c_int, c_char, c_char_p
from ctypes import POINTER as _P
from .dll import _bind, SDLFunc, AttributeDict
from .stdinc import Uint8

__all__ = [
    # Defines
    "SDL_GUID",
]


# Constants & typedefs

class SDL_GUID(Structure):
    _fields_ = [("data", (Uint8 * 16))]


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("SDL_GUIDToString", [SDL_GUID, _P(c_char), c_int], None, added='2.23.1'),
    SDLFunc("SDL_GUIDFromString", [c_char_p], SDL_GUID, added='2.23.1'),
]
_ctypes = AttributeDict()
for f in _funcdefs:
    _ctypes[f.name] = _bind(f.name, f.args, f.returns, f.added)
    __all__.append(f.name) # Add all bound functions to module namespace


# Aliases for ctypes bindings

def SDL_GUIDToString(guid, pszGUID, cbGUID):
    return _ctypes["SDL_GUIDToString"](guid, pszGUID, cbGUID)

def SDL_GUIDFromString(pchGUID):
    return _ctypes["SDL_GUIDFromString"](pchGUID)
