from ctypes import POINTER, c_int, c_void_p
from .dll import _bind
from .video import SDL_Window

__all__ = [
    # Opaque Types
    "SDL_MetalView",
    
    # Functions
    "SDL_Metal_CreateView", "SDL_Metal_DestroyView"
]

# NOTE: These functions are currently untested, but proper usage likely involves
# the use of pyobjc to create an NSView from the created SDL_MetalView.


SDL_MetalView = c_void_p

SDL_Metal_CreateView = _bind("SDL_Metal_CreateView", [POINTER(SDL_Window)], SDL_MetalView, added='2.0.12')
SDL_Metal_DestroyView = _bind("SDL_Metal_DestroyView", [SDL_MetalView], None, added='2.0.12')
