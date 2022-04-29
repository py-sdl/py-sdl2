from ctypes import c_int, c_void_p
from ctypes import POINTER as _P
from .dll import _bind
from .video import SDL_Window

# NOTE: These functions are currently untested, but proper usage likely involves
# the use of pyobjc to create an NSView from the created SDL_MetalView.

__all__ = [
    # Opaque Types
    "SDL_MetalView",
    
    # Functions
    "SDL_Metal_CreateView", "SDL_Metal_DestroyView", "SDL_Metal_GetLayer",
    "SDL_Metal_GetDrawableSize"
]


# Opaque typedefs

class SDL_MetalView(c_void_p):
    pass



SDL_Metal_CreateView = _bind("SDL_Metal_CreateView", [_P(SDL_Window)], SDL_MetalView, added='2.0.12')
SDL_Metal_DestroyView = _bind("SDL_Metal_DestroyView", [SDL_MetalView], None, added='2.0.12')
SDL_Metal_GetLayer = _bind("SDL_Metal_GetLayer", [SDL_MetalView], c_void_p, added='2.0.14')
SDL_Metal_GetDrawableSize = _bind("SDL_Metal_GetDrawableSize", [_P(SDL_Window), _P(c_int), _P(c_int)], None, added='2.0.14')
