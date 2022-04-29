from ctypes import Structure, c_int, c_char_p, c_void_p, c_float, c_double
from ctypes import POINTER as _P
from .dll import _bind
from .stdinc import Uint8, Uint32, SDL_bool
from .pixels import SDL_Color
from .blendmode import SDL_BlendMode
from .rect import SDL_Point, SDL_FPoint, SDL_Rect, SDL_FRect
from .surface import SDL_Surface
from .video import SDL_Window

__all__ = [
    # Structs & Opaque Types
    "SDL_RendererInfo", "SDL_Renderer", "SDL_Texture", "SDL_Vertex",

    # Enums
    "SDL_RendererFlags",
    "SDL_RENDERER_SOFTWARE", "SDL_RENDERER_ACCELERATED",
    "SDL_RENDERER_PRESENTVSYNC", "SDL_RENDERER_TARGETTEXTURE",

    "SDL_ScaleMode",
    "SDL_ScaleModeNearest", "SDL_ScaleModeLinear", "SDL_ScaleModeBest",

    "SDL_TextureAccess",
    "SDL_TEXTUREACCESS_STATIC", "SDL_TEXTUREACCESS_STREAMING",
    "SDL_TEXTUREACCESS_TARGET",

    "SDL_TextureModulate",
    "SDL_TEXTUREMODULATE_NONE", "SDL_TEXTUREMODULATE_COLOR",
    "SDL_TEXTUREMODULATE_ALPHA",

    "SDL_RendererFlip",
    "SDL_FLIP_NONE", "SDL_FLIP_HORIZONTAL", "SDL_FLIP_VERTICAL",

    # Functions
    "SDL_GetNumRenderDrivers", "SDL_GetRenderDriverInfo",
    "SDL_CreateWindowAndRenderer", "SDL_CreateRenderer",
    "SDL_CreateSoftwareRenderer", "SDL_GetRenderer",
    "SDL_GetRendererInfo", "SDL_CreateTexture",
    "SDL_CreateTextureFromSurface", "SDL_QueryTexture",
    "SDL_SetTextureColorMod", "SDL_GetTextureColorMod",
    "SDL_SetTextureAlphaMod", "SDL_GetTextureAlphaMod",
    "SDL_SetTextureBlendMode", "SDL_GetTextureBlendMode",
    "SDL_SetTextureScaleMode", "SDL_GetTextureScaleMode",
    "SDL_SetTextureUserData", "SDL_GetTextureUserData",
    "SDL_UpdateTexture", "SDL_LockTexture", "SDL_LockTextureToSurface",
    "SDL_UnlockTexture",
    "SDL_RenderTargetSupported", "SDL_SetRenderTarget",
    "SDL_GetRenderTarget", "SDL_RenderSetLogicalSize",
    "SDL_RenderGetLogicalSize", "SDL_RenderSetViewport",
    "SDL_RenderGetClipRect", "SDL_RenderSetClipRect",
    "SDL_RenderGetViewport", "SDL_RenderSetScale", "SDL_RenderGetScale",
    "SDL_RenderWindowToLogical", "SDL_RenderLogicalToWindow",
    "SDL_SetRenderDrawColor", "SDL_GetRenderDrawColor",
    "SDL_SetRenderDrawBlendMode", "SDL_GetRenderDrawBlendMode",
    "SDL_RenderClear", "SDL_RenderDrawPoint", "SDL_RenderDrawPoints",
    "SDL_RenderDrawLine", "SDL_RenderDrawLines", "SDL_RenderDrawRect",
    "SDL_RenderDrawRects", "SDL_RenderFillRect", "SDL_RenderFillRects",
    "SDL_RenderCopy", "SDL_RenderCopyEx", "SDL_RenderDrawPointF",
    "SDL_RenderDrawPointsF", "SDL_RenderDrawLineF",
    "SDL_RenderDrawLinesF", "SDL_RenderDrawRectF",
    "SDL_RenderDrawRectsF", "SDL_RenderFillRectF",
    "SDL_RenderFillRectsF", "SDL_RenderCopyF", "SDL_RenderCopyExF",
    "SDL_RenderGeometry", "SDL_RenderGeometryRaw",
    "SDL_RenderReadPixels", "SDL_RenderPresent",
    "SDL_DestroyTexture", "SDL_DestroyRenderer", "SDL_RenderFlush",
    "SDL_UpdateYUVTexture", "SDL_UpdateNVTexture",
    "SDL_GL_BindTexture", "SDL_GL_UnbindTexture",
    "SDL_GetRendererOutputSize", "SDL_RenderGetIntegerScale",
    "SDL_RenderSetIntegerScale", "SDL_RenderGetMetalLayer",
    "SDL_RenderGetMetalCommandEncoder", "SDL_RenderSetVSync"
]


# Constants & enums

SDL_RendererFlags = c_int
SDL_RENDERER_SOFTWARE = 0x00000001
SDL_RENDERER_ACCELERATED = 0x00000002
SDL_RENDERER_PRESENTVSYNC = 0x00000004
SDL_RENDERER_TARGETTEXTURE = 0x00000008

SDL_ScaleMode = c_int
SDL_ScaleModeNearest = 0
SDL_ScaleModeLinear = 1
SDL_ScaleModeBest = 2

SDL_TextureAccess = c_int
SDL_TEXTUREACCESS_STATIC = 0
SDL_TEXTUREACCESS_STREAMING = 1
SDL_TEXTUREACCESS_TARGET = 2

SDL_TextureModulate = c_int
SDL_TEXTUREMODULATE_NONE = 0x00000000
SDL_TEXTUREMODULATE_COLOR = 0x00000001
SDL_TEXTUREMODULATE_ALPHA = 0x00000002

SDL_RendererFlip = c_int
SDL_FLIP_NONE = 0x00000000
SDL_FLIP_HORIZONTAL = 0x00000001
SDL_FLIP_VERTICAL = 0x00000002


# Structs & opaque typedefs

class SDL_RendererInfo(Structure):
    _fields_ = [
        ("name", c_char_p),
        ("flags", Uint32),
        ("num_texture_formats", Uint32),
        ("texture_formats", Uint32 * 16),
        ("max_texture_width", c_int),
        ("max_texture_height", c_int),
    ]

class SDL_Vertex(Structure):
    _fields_ = [
        ("position", SDL_FPoint),
        ("color", SDL_Color),
        ("tex_coord", SDL_FPoint),
    ]

    def __init__(
        self, position=SDL_FPoint(), color=SDL_Color(), tex_coord=SDL_FPoint()
    ):
        super(SDL_Vertex, self).__init__()
        self.position = self._get_point(position, "position")
        self.color = self._get_color(color)
        self.tex_coord = self._get_point(tex_coord, "tex_coord")

    def _get_point(self, p, argname):
        if type(p) in (tuple, list) and len(p) == 2:
            p = SDL_FPoint(p[0], p[1])
        elif type(p) == SDL_FPoint:
            p = SDL_FPoint(p.x, p.y)
        else:
            err = "'{0}' must be an (x, y) tuple or an SDL_FPoint."
            raise ValueError(err.format(argname))
        return p

    def _get_color(self, col):
        if type(col).__name__ in ("Color", "SDL_Color"):
            col = SDL_Color(col.r, col.g, col.b, col.a)
        elif type(col) in (tuple, list) and len(col) in (3, 4):
            if len(col) == 3:
                col = SDL_Color(col[0], col[1], col[2], 255)
            else:
                col = SDL_Color(col[0], col[1], col[2], col[3])
        else:
            err = "'color' must be an RGBA tuple or an SDL_Color."
            raise ValueError(err)
        return col

    def __repr__(self):
        x = round(self.position.x, 4)
        y = round(self.position.y, 4)
        c = self.color
        col = str([c.r, c.g, c.b, c.a])
        return "SDL_Vertex(x={0}, y={1}, color={2})".format(x, y, col)

    def __copy__(self):
        return SDL_Vertex(self.position, self.color, self.tex_coord)

    def __deepcopy__(self, memo):
        return SDL_Vertex(self.position, self.color, self.tex_coord)

class SDL_Renderer(c_void_p):
    pass

class SDL_Texture(c_void_p):
    pass



SDL_GetNumRenderDrivers = _bind("SDL_GetNumRenderDrivers", None, c_int)
SDL_GetRenderDriverInfo = _bind("SDL_GetRenderDriverInfo", [c_int, _P(SDL_RendererInfo)], c_int)
SDL_CreateWindowAndRenderer = _bind("SDL_CreateWindowAndRenderer", [c_int, c_int, Uint32, _P(_P(SDL_Window)), _P(_P(SDL_Renderer))], c_int)
SDL_CreateRenderer = _bind("SDL_CreateRenderer", [_P(SDL_Window), c_int, Uint32], _P(SDL_Renderer))
SDL_CreateSoftwareRenderer = _bind("SDL_CreateSoftwareRenderer", [_P(SDL_Surface)], _P(SDL_Renderer))
SDL_GetRenderer = _bind("SDL_GetRenderer", [_P(SDL_Window)], _P(SDL_Renderer))
SDL_GetRendererInfo = _bind("SDL_GetRendererInfo", [_P(SDL_Renderer), _P(SDL_RendererInfo)], c_int)
SDL_GetRendererOutputSize = _bind("SDL_GetRendererOutputSize", [_P(SDL_Renderer), _P(c_int), _P(c_int)], c_int)
SDL_CreateTexture = _bind("SDL_CreateTexture", [_P(SDL_Renderer), Uint32, c_int, c_int, c_int], _P(SDL_Texture))
SDL_CreateTextureFromSurface = _bind("SDL_CreateTextureFromSurface", [_P(SDL_Renderer), _P(SDL_Surface)], _P(SDL_Texture))
SDL_QueryTexture = _bind("SDL_QueryTexture", [_P(SDL_Texture), _P(Uint32), _P(c_int), _P(c_int), _P(c_int)], c_int)
SDL_SetTextureColorMod = _bind("SDL_SetTextureColorMod", [_P(SDL_Texture), Uint8, Uint8, Uint8], c_int)
SDL_GetTextureColorMod = _bind("SDL_GetTextureColorMod", [_P(SDL_Texture), _P(Uint8), _P(Uint8), _P(Uint8)], c_int)
SDL_SetTextureAlphaMod = _bind("SDL_SetTextureAlphaMod", [_P(SDL_Texture), Uint8], c_int)
SDL_GetTextureAlphaMod = _bind("SDL_GetTextureAlphaMod", [_P(SDL_Texture), _P(Uint8)], c_int)
SDL_SetTextureBlendMode = _bind("SDL_SetTextureBlendMode", [_P(SDL_Texture), SDL_BlendMode], c_int)
SDL_GetTextureBlendMode = _bind("SDL_GetTextureBlendMode", [_P(SDL_Texture), _P(SDL_BlendMode)], c_int)
SDL_SetTextureScaleMode = _bind("SDL_SetTextureScaleMode", [_P(SDL_Texture), SDL_ScaleMode], c_int, added='2.0.12')
SDL_GetTextureScaleMode = _bind("SDL_GetTextureScaleMode", [_P(SDL_Texture), _P(SDL_ScaleMode)], c_int, added='2.0.12')
SDL_SetTextureUserData = _bind("SDL_SetTextureUserData", [_P(SDL_Texture), c_void_p], c_int, added='2.0.18')
SDL_GetTextureUserData = _bind("SDL_GetTextureUserData", [_P(SDL_Texture)], c_void_p, added='2.0.18')
SDL_UpdateTexture = _bind("SDL_UpdateTexture", [_P(SDL_Texture), _P(SDL_Rect), c_void_p, c_int], c_int)
SDL_UpdateYUVTexture = _bind("SDL_UpdateYUVTexture", [_P(SDL_Texture), _P(SDL_Rect), _P(Uint8), c_int, _P(Uint8), c_int, _P(Uint8), c_int], c_int)
SDL_UpdateNVTexture = _bind("SDL_UpdateNVTexture", [_P(SDL_Texture), _P(SDL_Rect), _P(Uint8), c_int, _P(Uint8), c_int], c_int, added='2.0.16')
SDL_LockTexture = _bind("SDL_LockTexture", [_P(SDL_Texture), _P(SDL_Rect), _P(c_void_p), _P(c_int)], c_int)
SDL_LockTextureToSurface = _bind("SDL_LockTextureToSurface", [_P(SDL_Texture), _P(SDL_Rect), _P(_P(SDL_Surface))], c_int, added='2.0.12')
SDL_UnlockTexture = _bind("SDL_UnlockTexture", [_P(SDL_Texture)])
SDL_RenderTargetSupported = _bind("SDL_RenderTargetSupported", [_P(SDL_Renderer)], SDL_bool)
SDL_SetRenderTarget = _bind("SDL_SetRenderTarget", [_P(SDL_Renderer), _P(SDL_Texture)], c_int)
SDL_GetRenderTarget = _bind("SDL_GetRenderTarget", [_P(SDL_Renderer)], _P(SDL_Texture))
SDL_RenderSetLogicalSize = _bind("SDL_RenderSetLogicalSize", [_P(SDL_Renderer), c_int, c_int], c_int)
SDL_RenderGetLogicalSize = _bind("SDL_RenderGetLogicalSize", [_P(SDL_Renderer), _P(c_int), _P(c_int)])
SDL_RenderSetIntegerScale = _bind("SDL_RenderSetIntegerScale", [_P(SDL_Renderer), SDL_bool], c_int, added='2.0.5')
SDL_RenderGetIntegerScale = _bind("SDL_RenderGetIntegerScale", [_P(SDL_Renderer)], SDL_bool, added='2.0.5')
SDL_RenderSetViewport = _bind("SDL_RenderSetViewport", [_P(SDL_Renderer), _P(SDL_Rect)], c_int)
SDL_RenderGetViewport = _bind("SDL_RenderGetViewport", [_P(SDL_Renderer), _P(SDL_Rect)])
SDL_RenderGetClipRect = _bind("SDL_RenderGetClipRect", [_P(SDL_Renderer), _P(SDL_Rect)])
SDL_RenderSetClipRect = _bind("SDL_RenderSetClipRect", [_P(SDL_Renderer), _P(SDL_Rect)], c_int)
SDL_RenderIsClipEnabled = _bind("SDL_RenderIsClipEnabled", [_P(SDL_Renderer)], SDL_bool, added='2.0.4')
SDL_RenderSetScale = _bind("SDL_RenderSetScale", [_P(SDL_Renderer), c_float, c_float], c_int)
SDL_RenderGetScale = _bind("SDL_RenderGetScale", [_P(SDL_Renderer), _P(c_float), _P(c_float)])
SDL_RenderWindowToLogical = _bind("SDL_RenderWindowToLogical", [_P(SDL_Renderer), c_int, c_int, _P(c_float), _P(c_float)], added='2.0.18')
SDL_RenderLogicalToWindow = _bind("SDL_RenderLogicalToWindow", [_P(SDL_Renderer), c_float, c_float, _P(c_int), _P(c_int)], added='2.0.18')
SDL_SetRenderDrawColor = _bind("SDL_SetRenderDrawColor", [_P(SDL_Renderer), Uint8, Uint8, Uint8, Uint8], c_int)
SDL_GetRenderDrawColor = _bind("SDL_GetRenderDrawColor", [_P(SDL_Renderer), _P(Uint8), _P(Uint8), _P(Uint8), _P(Uint8)], c_int)
SDL_SetRenderDrawBlendMode = _bind("SDL_SetRenderDrawBlendMode", [_P(SDL_Renderer), SDL_BlendMode], c_int)
SDL_GetRenderDrawBlendMode = _bind("SDL_GetRenderDrawBlendMode", [_P(SDL_Renderer), _P(SDL_BlendMode)], c_int)
SDL_RenderClear = _bind("SDL_RenderClear", [_P(SDL_Renderer)], c_int)
SDL_RenderDrawPoint = _bind("SDL_RenderDrawPoint", [_P(SDL_Renderer), c_int, c_int], c_int)
SDL_RenderDrawPoints = _bind("SDL_RenderDrawPoints", [_P(SDL_Renderer), _P(SDL_Point), c_int], c_int)
SDL_RenderDrawLine = _bind("SDL_RenderDrawLine", [_P(SDL_Renderer), c_int, c_int, c_int, c_int], c_int)
SDL_RenderDrawLines = _bind("SDL_RenderDrawLines", [_P(SDL_Renderer), _P(SDL_Point), c_int], c_int)
SDL_RenderDrawRect = _bind("SDL_RenderDrawRect", [_P(SDL_Renderer), _P(SDL_Rect)], c_int)
SDL_RenderDrawRects = _bind("SDL_RenderDrawRects", [_P(SDL_Renderer), _P(SDL_Rect), c_int], c_int)
SDL_RenderFillRect = _bind("SDL_RenderFillRect", [_P(SDL_Renderer), _P(SDL_Rect)], c_int)
SDL_RenderFillRects = _bind("SDL_RenderFillRects", [_P(SDL_Renderer), _P(SDL_Rect), c_int], c_int)
SDL_RenderCopy = _bind("SDL_RenderCopy", [_P(SDL_Renderer), _P(SDL_Texture), _P(SDL_Rect), _P(SDL_Rect)], c_int)
SDL_RenderCopyEx = _bind("SDL_RenderCopyEx", [_P(SDL_Renderer), _P(SDL_Texture), _P(SDL_Rect), _P(SDL_Rect), c_double, _P(SDL_Point), SDL_RendererFlip], c_int)
SDL_RenderDrawPointF = _bind("SDL_RenderDrawPointF", [_P(SDL_Renderer), c_float, c_float], c_int, added='2.0.10')
SDL_RenderDrawPointsF = _bind("SDL_RenderDrawPointsF", [_P(SDL_Renderer), _P(SDL_FPoint), c_int], c_int, added='2.0.10')
SDL_RenderDrawLineF = _bind("SDL_RenderDrawLineF", [_P(SDL_Renderer), c_float, c_float, c_float, c_float], c_int, added='2.0.10')
SDL_RenderDrawLinesF = _bind("SDL_RenderDrawLinesF", [_P(SDL_Renderer), _P(SDL_FPoint), c_int], c_int, added='2.0.10')
SDL_RenderDrawRectF = _bind("SDL_RenderDrawRectF", [_P(SDL_Renderer), _P(SDL_FRect)], c_int, added='2.0.10')
SDL_RenderDrawRectsF = _bind("SDL_RenderDrawRectsF", [_P(SDL_Renderer), _P(SDL_FRect), c_int], c_int, added='2.0.10')
SDL_RenderFillRectF = _bind("SDL_RenderFillRectF", [_P(SDL_Renderer), _P(SDL_FRect)], c_int, added='2.0.10')
SDL_RenderFillRectsF = _bind("SDL_RenderFillRectsF", [_P(SDL_Renderer), _P(SDL_FRect), c_int], c_int, added='2.0.10')
SDL_RenderCopyF = _bind("SDL_RenderCopyF", [_P(SDL_Renderer), _P(SDL_Texture), _P(SDL_Rect), _P(SDL_FRect)], c_int, added='2.0.10')
SDL_RenderCopyExF = _bind("SDL_RenderCopyExF", [_P(SDL_Renderer), _P(SDL_Texture), _P(SDL_Rect), _P(SDL_FRect), c_double, _P(SDL_FPoint), SDL_RendererFlip], c_int, added='2.0.10')
SDL_RenderGeometry = _bind("SDL_RenderGeometry", [_P(SDL_Renderer), _P(SDL_Texture), _P(SDL_Vertex), c_int, _P(c_int), c_int], c_int, added='2.0.18')
SDL_RenderGeometryRaw = _bind("SDL_RenderGeometryRaw", [_P(SDL_Renderer), _P(SDL_Texture), _P(c_float), c_int, _P(SDL_Color), c_int, _P(c_float), c_int, c_int, c_void_p, c_int, c_int], c_int, added='2.0.18')
SDL_RenderReadPixels = _bind("SDL_RenderReadPixels", [_P(SDL_Renderer), _P(SDL_Rect), Uint32, c_void_p, c_int], c_int)
SDL_RenderPresent = _bind("SDL_RenderPresent", [_P(SDL_Renderer)])
SDL_DestroyTexture = _bind("SDL_DestroyTexture", [_P(SDL_Texture)])
SDL_DestroyRenderer = _bind("SDL_DestroyRenderer", [_P(SDL_Renderer)])
SDL_RenderFlush = _bind("SDL_RenderFlush", [_P(SDL_Renderer)], c_int, added='2.0.10')
SDL_GL_BindTexture = _bind("SDL_GL_BindTexture", [_P(SDL_Texture), _P(c_float), _P(c_float)], c_int)
SDL_GL_UnbindTexture = _bind("SDL_GL_UnbindTexture", [_P(SDL_Texture)], c_int)
SDL_RenderGetMetalLayer = _bind("SDL_RenderGetMetalLayer", [_P(SDL_Renderer)], c_void_p, added='2.0.8')
SDL_RenderGetMetalCommandEncoder = _bind("SDL_RenderGetMetalCommandEncoder", [_P(SDL_Renderer)], c_void_p, added='2.0.8')
SDL_RenderSetVSync = _bind("SDL_RenderSetVSync", [_P(SDL_Renderer), c_int], c_int, added='2.0.18')
