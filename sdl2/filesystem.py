from ctypes import c_char, c_char_p
from .dll import _bind, SDLFunc, AttributeDict

__all__ = ["SDL_GetBasePath", "SDL_GetPrefPath"]


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("SDL_GetBasePath", None, c_char_p),
    SDLFunc("SDL_GetPrefPath", [c_char_p, c_char_p], c_char_p),
]
_ctypes = AttributeDict()
for f in _funcdefs:
    _ctypes[f.name] = _bind(f.name, f.args, f.returns, f.added)


# Aliases for ctypes bindings

SDL_GetBasePath = _ctypes["SDL_GetBasePath"]
SDL_GetPrefPath = _ctypes["SDL_GetPrefPath"]
