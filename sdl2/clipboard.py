from ctypes import c_char_p, c_int
from .dll import _bind, SDLFunc, AttributeDict
from .stdinc import SDL_bool

__all__ = []


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("SDL_SetClipboardText", [c_char_p], c_int),
    SDLFunc("SDL_GetClipboardText", None, c_char_p),
    SDLFunc("SDL_HasClipboardText", None, SDL_bool),
]
_ctypes = AttributeDict()
for f in _funcdefs:
    _ctypes[f.name] = _bind(f.name, f.args, f.returns, f.added)
    __all__.append(f.name) # Add all bound functions to module namespace


# Aliases for ctypes bindings

SDL_SetClipboardText = _ctypes["SDL_SetClipboardText"]
SDL_GetClipboardText = _ctypes["SDL_GetClipboardText"]
SDL_HasClipboardText = _ctypes["SDL_HasClipboardText"]
