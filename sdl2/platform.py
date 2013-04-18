from ctypes import c_char_p
from .dll import _bind

SDL_GetPlatform = _bind("SDL_GetPlatform", None, c_char_p)
