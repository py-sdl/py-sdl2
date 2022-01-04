import os
from ctypes import POINTER, c_int, c_char_p
from ctypes import POINTER as _P
from .dll import DLL, SDLFunc
from .version import SDL_version, SDL_VERSIONNUM
from .surface import SDL_Surface
from .rwops import SDL_RWops
from .render import SDL_Texture, SDL_Renderer
from .error import SDL_SetError, SDL_GetError

__all__ = [
    # Defines
    "SDL_IMAGE_MAJOR_VERSION", "SDL_IMAGE_MINOR_VERSION", "SDL_IMAGE_PATCHLEVEL",

    # Enums
    "IMG_InitFlags",
    "IMG_INIT_JPG", "IMG_INIT_PNG", "IMG_INIT_TIF", "IMG_INIT_WEBP",
    
    # Macro Functions
    "SDL_IMAGE_VERSION", "SDL_IMAGE_COMPILEDVERSION",
    "SDL_IMAGE_VERSION_ATLEAST", 
    
    # Functions
    "IMG_Linked_Version", "IMG_Init", "IMG_Quit", "IMG_LoadTyped_RW",
    "IMG_Load", "IMG_Load_RW", "IMG_LoadTexture", "IMG_LoadTexture_RW",
    "IMG_LoadTextureTyped_RW", "IMG_isICO", "IMG_isCUR", "IMG_isBMP",
    "IMG_isGIF", "IMG_isJPG", "IMG_isLBM", "IMG_isPNG", "IMG_isPNM",
    "IMG_isPCX", "IMG_isTIF", "IMG_isXCF", "IMG_isXV", "IMG_isWEBP",
    "IMG_LoadBMP_RW", "IMG_LoadCUR_RW", "IMG_LoadCUR_RW",
    "IMG_LoadGIF_RW", "IMG_LoadICO_RW", "IMG_LoadJPG_RW",
    "IMG_LoadLBM_RW", "IMG_LoadPCX_RW", "IMG_LoadPNM_RW",
    "IMG_LoadPNG_RW", "IMG_LoadTGA_RW", "IMG_LoadTIF_RW",
    "IMG_LoadXCF_RW", "IMG_LoadWEBP_RW", "IMG_LoadXPM_RW",
    "IMG_LoadXV_RW", "IMG_ReadXPMFromArray",
    "IMG_GetError", "IMG_SetError", "IMG_SaveJPG", "IMG_SaveJPG_RW",
    
    # Python Functions
    "get_dll_file"
]


try:
    dll = DLL("SDL2_image", ["SDL2_image", "SDL2_image-2.0"],
              os.getenv("PYSDL2_DLL_PATH"))
except RuntimeError as exc:
    raise ImportError(exc)


def get_dll_file():
    """Gets the file name of the loaded SDL2_image library."""
    return dll.libfile

_bind = dll.bind_function


# Constants, enums, type definitions, and macros

SDL_IMAGE_MAJOR_VERSION = 2
SDL_IMAGE_MINOR_VERSION = 0
SDL_IMAGE_PATCHLEVEL = 5

def SDL_IMAGE_VERSION(x):
    x.major = SDL_IMAGE_MAJOR_VERSION
    x.minor = SDL_IMAGE_MINOR_VERSION
    x.patch = SDL_IMAGE_PATCHLEVEL

SDL_IMAGE_COMPILEDVERSION = SDL_VERSIONNUM(SDL_IMAGE_MAJOR_VERSION, SDL_IMAGE_MINOR_VERSION, SDL_IMAGE_PATCHLEVEL)
SDL_IMAGE_VERSION_ATLEAST = lambda x, y, z: (SDL_IMAGE_COMPILEDVERSION >= SDL_VERSIONNUM(x, y, z))

IMG_InitFlags = c_int
IMG_INIT_JPG = 0x00000001
IMG_INIT_PNG = 0x00000002
IMG_INIT_TIF = 0x00000004
IMG_INIT_WEBP = 0x00000008


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("IMG_Linked_Version", None, _P(SDL_version)),
    SDLFunc("IMG_Init", [c_int], c_int),
    SDLFunc("IMG_Quit"),
    SDLFunc("IMG_LoadTyped_RW", [_P(SDL_RWops), c_int, c_char_p], _P(SDL_Surface)),
    SDLFunc("IMG_Load", [c_char_p], _P(SDL_Surface)),
    SDLFunc("IMG_Load_RW", [_P(SDL_RWops), c_int], _P(SDL_Surface)),
    SDLFunc("IMG_LoadTexture", [_P(SDL_Renderer), c_char_p], _P(SDL_Texture)),
    SDLFunc("IMG_LoadTexture_RW", [_P(SDL_Renderer), _P(SDL_RWops), c_int], _P(SDL_Texture)),
    SDLFunc("IMG_LoadTextureTyped_RW", [_P(SDL_Renderer), _P(SDL_RWops), c_int, c_char_p], _P(SDL_Texture)),
    SDLFunc("IMG_isICO", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isCUR", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isBMP", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isGIF", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isJPG", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isLBM", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isPCX", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isPNG", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isPNM", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isSVG", [_P(SDL_RWops)], c_int, added='2.0.2'),
    SDLFunc("IMG_isTIF", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isXCF", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isXPM", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isXV", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_isWEBP", [_P(SDL_RWops)], c_int),
    SDLFunc("IMG_LoadICO_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadCUR_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadBMP_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadGIF_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadJPG_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadLBM_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadPCX_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadPNG_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadPNM_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadSVG_RW", [_P(SDL_RWops)], _P(SDL_Surface), added='2.0.2'),
    SDLFunc("IMG_LoadTGA_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadTIF_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadXCF_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadXPM_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadXV_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_LoadWEBP_RW", [_P(SDL_RWops)], _P(SDL_Surface)),
    SDLFunc("IMG_ReadXPMFromArray", [_P(c_char_p)], _P(SDL_Surface)),
    SDLFunc("IMG_SaveJPG", [_P(SDL_Surface), c_char_p, c_int], c_int, added='2.0.2'),
    SDLFunc("IMG_SaveJPG_RW", [_P(SDL_Surface), _P(SDL_RWops), c_int, c_int], c_int, added='2.0.2'),
    SDLFunc("IMG_SavePNG", [_P(SDL_Surface), c_char_p], c_int),
    SDLFunc("IMG_SavePNG_RW", [_P(SDL_Surface), _P(SDL_RWops), c_int], c_int),
]
_funcs = {}
for f in _funcdefs:
    _funcs[f.name] = _bind(f.name, f.args, f.returns, f.added)


# Python wrapper functions

def IMG_Linked_Version():
    return _funcs["IMG_Linked_Version"]()

def IMG_Init(flags):
    return _funcs["IMG_Init"](flags)

def IMG_Quit():
    return _funcs["IMG_Quit"]()

def IMG_LoadTyped_RW(src, freesrc, type):
    return _funcs["IMG_LoadTyped_RW"](src, freesrc, type)

def IMG_Load(file):
    return _funcs["IMG_Load"](file)

def IMG_Load_RW(src, freesrc):
    return _funcs["IMG_Load_RW"](src, freesrc)

def IMG_LoadTexture(renderer, file):
    return _funcs["IMG_LoadTexture"](renderer, file)

def IMG_LoadTexture_RW(renderer, src, freesrc):
    return _funcs["IMG_LoadTexture_RW"](renderer, src, freesrc)

def IMG_LoadTextureTyped_RW(renderer, src, freesrc, type):
    return _funcs["IMG_LoadTextureTyped_RW"](renderer, src, freesrc, type)


def IMG_isICO(src):
    return _funcs["IMG_isICO"](src)

def IMG_isCUR(src):
    return _funcs["IMG_isCUR"](src)

def IMG_isBMP(src):
    return _funcs["IMG_isBMP"](src)

def IMG_isGIF(src):
    return _funcs["IMG_isGIF"](src)

def IMG_isJPG(src):
    return _funcs["IMG_isJPG"](src)

def IMG_isLBM(src):
    return _funcs["IMG_isLBM"](src)

def IMG_isPCX(src):
    return _funcs["IMG_isPCX"](src)

def IMG_isPNG(src):
    return _funcs["IMG_isPNG"](src)

def IMG_isPNM(src):
    return _funcs["IMG_isPNM"](src)

def IMG_isSVG(src):
    return _funcs["IMG_isSVG"](src)

def IMG_isTIF(src):
    return _funcs["IMG_isTIF"](src)

def IMG_isXCF(src):
    return _funcs["IMG_isXCF"](src)

def IMG_isXPM(src):
    return _funcs["IMG_isXPM"](src)

def IMG_isXV(src):
    return _funcs["IMG_isXV"](src)

def IMG_isWEBP(src):
    return _funcs["IMG_isWEBP"](src)


def IMG_LoadICO_RW(src):
    return _funcs["IMG_LoadICO_RW"](src)

def IMG_LoadCUR_RW(src):
    return _funcs["IMG_LoadCUR_RW"](src)

def IMG_LoadBMP_RW(src):
    return _funcs["IMG_LoadBMP_RW"](src)

def IMG_LoadGIF_RW(src):
    return _funcs["IMG_LoadGIF_RW"](src)

def IMG_LoadJPG_RW(src):
    return _funcs["IMG_LoadJPG_RW"](src)

def IMG_LoadLBM_RW(src):
    return _funcs["IMG_LoadLBM_RW"](src)

def IMG_LoadPCX_RW(src):
    return _funcs["IMG_LoadPCX_RW"](src)

def IMG_LoadPNG_RW(src):
    return _funcs["IMG_LoadPNG_RW"](src)

def IMG_LoadPNM_RW(src):
    return _funcs["IMG_LoadPNM_RW"](src)

def IMG_LoadSVG_RW(src):
    return _funcs["IMG_LoadSVG_RW"](src)

def IMG_LoadTGA_RW(src):
    return _funcs["IMG_LoadTGA_RW"](src)

def IMG_LoadTIF_RW(src):
    return _funcs["IMG_LoadTIF_RW"](src)

def IMG_LoadXCF_RW(src):
    return _funcs["IMG_LoadXCF_RW"](src)

def IMG_LoadXPM_RW(src):
    return _funcs["IMG_LoadXPM_RW"](src)

def IMG_LoadXV_RW(src):
    return _funcs["IMG_LoadXV_RW"](src)

def IMG_LoadWEBP_RW(src):
    return _funcs["IMG_LoadWEBP_RW"](src)


def IMG_ReadXPMFromArray(xpm):
    return _funcs["IMG_ReadXPMFromArray"](xpm)


def IMG_SavePNG(surface, file):
    return _funcs["IMG_SavePNG"](surface, file)

def IMG_SavePNG_RW(surface, dst, freedst):
    return _funcs["IMG_SavePNG_RW"](surface, dst, freedst)

def IMG_SaveJPG(surface, file, quality):
    # NOTE: Not available in official macOS binaries
    return _funcs["IMG_SaveJPG"](surface, file, quality)

def IMG_SaveJPG_RW(surface, dst, freedst, quality):
    # NOTE: Not available in official macOS binaries
    return _funcs["IMG_SaveJPG_RW"](surface, dst, freedst, quality)


IMG_SetError = SDL_SetError
IMG_GetError = SDL_GetError
