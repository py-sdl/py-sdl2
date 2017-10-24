from ctypes import c_char, c_char_p, POINTER
from .dll import _bind

__all__ = ["SDL_GetBasePath", "SDL_GetPrefPath"]

SDL_GetBasePath = _bind("SDL_GetBasePath", None, POINTER(c_char))
SDL_GetPrefPath = _bind("SDL_GetPrefPath", [c_char_p, c_char_p], POINTER(c_char))
