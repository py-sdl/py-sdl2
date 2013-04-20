"""SDL2 wrapper package"""
from .dll import get_dll_file, _bind
from ctypes import c_int
from .stdinc import Uint32

__all__ = ["SDL_INIT_TIMER", "SDL_INIT_AUDIO", "SDL_INIT_VIDEO",
           "SDL_INIT_JOYSTICK", "SDL_INIT_HAPTIC", "SDL_INIT_GAMECONTROLLER",
           "SDL_INIT_NOPARACHUTE", "SDL_INIT_EVERYTHING", "SDL_Init",
           "SDL_InitSubSystem", "SDL_QuitSubSystem", "SDL_WasInit", "SDL_Quit",
           "version_info"
           ]

SDL_INIT_TIMER = 0x00000001
SDL_INIT_AUDIO = 0x00000010
SDL_INIT_VIDEO = 0x00000020
SDL_INIT_JOYSTICK = 0x00000200
SDL_INIT_HAPTIC = 0x00001000
SDL_INIT_GAMECONTROLLER = 0x00002000
SDL_INIT_NOPARACHUTE = 0x00100000
SDL_INIT_EVERYTHING = 0x0000FFFF

SDL_Init = _bind("SDL_Init", [Uint32], c_int)
SDL_InitSubSystem = _bind("SDL_InitSubSystem", [Uint32], c_int)
SDL_QuitSubSystem = _bind("SDL_QuitSubSystem", [Uint32])
SDL_WasInit = _bind("SDL_WasInit", [Uint32], Uint32)
SDL_Quit = _bind("SDL_Quit")

__version__ = "0.1.0"
version_info = (0, 1, 0, "")
