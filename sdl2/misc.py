from ctypes import c_char_p, c_int
from .dll import _bind, SDLFunc, AttributeDict

__all__ = [
    # Functions
    "SDL_OpenURL"
]


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("SDL_OpenURL", [c_char_p], c_int, added='2.0.14'),
]
_ctypes = AttributeDict()
for f in _funcdefs:
    _ctypes[f.name] = _bind(f.name, f.args, f.returns, f.added)


# Aliases for ctypes bindings

SDL_OpenURL = _ctypes["SDL_OpenURL"]
