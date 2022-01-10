from ctypes import byref, c_int, c_float, cast, POINTER

from .. import blendmode, surface, rect, video, render
from ..stdinc import Uint8

from .color import convert_to_color
from .common import SDLError
from .compat import deprecated
from .sprite import SoftwareSprite, TextureSprite
from .window import Window

__all__ = ["Renderer"]


class Renderer(object):
    """SDL2-based renderer for windows and sprites."""
    def __init__(self, target, index=-1, logical_size=None,
                 flags=render.SDL_RENDERER_ACCELERATED):
        """Creates a new Renderer for the given target.

        If target is a Window or SDL_Window, index and flags are passed
        to the relevant sdl.render.create_renderer() call. If target is
        a SoftwareSprite or SDL_Surface, the index and flags arguments are
        ignored.
        """
        self.sdlrenderer = None
        self.rendertarget = None
        if isinstance(target, Window):
            self.sdlrenderer = render.SDL_CreateRenderer(target.window, index,
                                                         flags)
        elif isinstance(target, video.SDL_Window):
            self.sdlrenderer = render.SDL_CreateRenderer(target, index, flags)
        elif isinstance(target, SoftwareSprite):
            self.sdlrenderer = render.SDL_CreateSoftwareRenderer(target.surface)
        elif isinstance(target, surface.SDL_Surface):
            self.sdlrenderer = render.SDL_CreateSoftwareRenderer(target)
        elif "SDL_Surface" in str(type(target)):
            self.sdlrenderer = render.SDL_CreateSoftwareRenderer(target.contents)
        else:
            raise TypeError("unsupported target type")

        self.rendertarget = target
        if logical_size is not None:
            self.logical_size = logical_size

    def __del__(self):
        if self.sdlrenderer:
            render.SDL_DestroyRenderer(self.sdlrenderer)
        self.sdlrenderer = None
        self.rendertarget = None

    @property
    @deprecated
    def renderer(self):
        return self.sdlrenderer

    @property
    def logical_size(self):
        """The logical pixel size of the Renderer"""
        w, h = c_int(), c_int()
        render.SDL_RenderGetLogicalSize(self.sdlrenderer, byref(w), byref(h))
        return w.value, h.value

    @logical_size.setter
    def logical_size(self, size):
        """The logical pixel size of the Renderer"""
        width, height = size
        ret = render.SDL_RenderSetLogicalSize(self.sdlrenderer, width, height)
        if ret != 0:
            raise SDLError()

    @property
    def color(self):
        """The drawing color of the Renderer."""
        r, g, b, a = Uint8(), Uint8(), Uint8(), Uint8()
        ret = render.SDL_GetRenderDrawColor(self.sdlrenderer, byref(r), byref(g),
                                            byref(b), byref(a))
        if ret == -1:
            raise SDLError()
        return convert_to_color((r.value, g.value, b.value, a.value))

    @color.setter
    def color(self, value):
        """The drawing color of the Renderer."""
        c = convert_to_color(value)
        ret = render.SDL_SetRenderDrawColor(self.sdlrenderer, c.r, c.g, c.b, c.a)
        if ret == -1:
            raise SDLError()

    @property
    def blendmode(self):
        """The blend mode used for drawing operations (fill and line)."""
        mode = blendmode.SDL_BlendMode()
        ret = render.SDL_GetRenderDrawBlendMode(self.sdlrenderer, byref(mode))
        if ret == -1:
            raise SDLError()
        return mode

    @blendmode.setter
    def blendmode(self, value):
        """The blend mode used for drawing operations (fill and line)."""
        ret = render.SDL_SetRenderDrawBlendMode(self.sdlrenderer, value)
        if ret == -1:
            raise SDLError()

    @property
    def scale(self):
        """The horizontal and vertical drawing scale."""
        sx = c_float(0.0)
        sy = c_float(0.0)
        render.SDL_RenderGetScale(self.sdlrenderer, byref(sx), byref(sy))
        return sx.value, sy.value

    @scale.setter
    def scale(self, value):
        """The horizontal and vertical drawing scale."""
        ret = render.SDL_RenderSetScale(self.sdlrenderer, value[0], value[1])
        if ret != 0:
            raise SDLError()

    def clear(self, color=None):
        """Clears the renderer with the currently set or passed color."""
        if color is not None:
            tmp = self.color
            self.color = color
        ret = render.SDL_RenderClear(self.sdlrenderer)
        if color is not None:
            self.color = tmp
        if ret == -1:
            raise SDLError()

    def copy(self, src, srcrect=None, dstrect=None, angle=0, center=None,
             flip=render.SDL_FLIP_NONE):
        """Copies (blits) the passed source to the target of the Renderer."""
        if isinstance(src, TextureSprite):
            texture = src.texture
            angle = angle or src.angle
            center = center or src.center
            flip = flip or src.flip
        elif isinstance(src, render.SDL_Texture):
            texture = src
        else:
            raise TypeError("src must be a TextureSprite or SDL_Texture")
        if srcrect is not None:
            x, y, w, h = srcrect
            srcrect = rect.SDL_Rect(x, y, w, h)
        if dstrect is not None:
            x, y, w, h = dstrect
            dstrect = rect.SDL_Rect(x, y, w, h)
        ret = render.SDL_RenderCopyEx(self.sdlrenderer, texture, srcrect,
                                      dstrect, angle, center, flip)
        if ret == -1:
            raise SDLError()

    def present(self):
        """Refreshes the target of the Renderer."""
        render.SDL_RenderPresent(self.sdlrenderer)

    def draw_line(self, points, color=None):
        """Draws one or multiple connected lines on the renderer."""
        # (x1, y1, x2, y2, ...)
        pcount = len(points)
        if (pcount % 2) != 0:
            raise ValueError("points does not contain a valid set of points")
        if pcount < 4:
            raise ValueError("points must contain more that one point")
        if pcount == 4:
            if color is not None:
                tmp = self.color
                self.color = color
            x1, y1, x2, y2 = points
            ret = render.SDL_RenderDrawLine(self.sdlrenderer, x1, y1, x2, y2)
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()
        else:
            x = 0
            off = 0
            count = pcount // 2
            SDL_Point = rect.SDL_Point
            ptlist = (SDL_Point * count)()
            while x < pcount:
                ptlist[off] = SDL_Point(points[x], points[x + 1])
                x += 2
                off += 1
            if color is not None:
                tmp = self.color
                self.color = color
            ptr = cast(ptlist, POINTER(SDL_Point))
            ret = render.SDL_RenderDrawLines(self.sdlrenderer, ptr, count)
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()

    def draw_point(self, points, color=None):
        """Draws one or multiple points on the renderer."""
        # (x1, y1, x2, y2, ...)
        pcount = len(points)
        if (pcount % 2) != 0:
            raise ValueError("points does not contain a valid set of points")
        if pcount == 2:
            if color is not None:
                tmp = self.color
                self.color = color
            ret = render.SDL_RenderDrawPoint(self.sdlrenderer, points[0],
                                             points[1])
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()
        else:
            x = 0
            off = 0
            count = pcount // 2
            SDL_Point = rect.SDL_Point
            ptlist = (SDL_Point * count)()
            while x < pcount:
                ptlist[off] = SDL_Point(points[x], points[x + 1])
                x += 2
                off += 1
            if color is not None:
                tmp = self.color
                self.color = color
            ptr = cast(ptlist, POINTER(SDL_Point))
            ret = render.SDL_RenderDrawPoints(self.sdlrenderer, ptr, count)
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()

    def draw_rect(self, rects, color=None):
        """Draws one or multiple rectangles on the renderer."""
        SDL_Rect = rect.SDL_Rect
        # ((x, y, w, h), ...)
        if type(rects[0]) == int:
            # single rect
            if color is not None:
                tmp = self.color
                self.color = color
            x, y, w, h = rects
            ret = render.SDL_RenderDrawRect(self.sdlrenderer, SDL_Rect(x, y, w, h))
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()
        else:
            x = 0
            rlist = (SDL_Rect * len(rects))()
            for idx, r in enumerate(rects):
                rlist[idx] = SDL_Rect(r[0], r[1], r[2], r[3])
            if color is not None:
                tmp = self.color
                self.color = color
            ptr = cast(rlist, POINTER(SDL_Rect))
            ret = render.SDL_RenderDrawRects(self.sdlrenderer, ptr, len(rects))
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()

    def fill(self, rects, color=None):
        """Fills one or multiple rectangular areas on the renderer."""
        SDL_Rect = rect.SDL_Rect
        # ((x, y, w, h), ...)
        if type(rects[0]) == int:
            # single rect
            if color is not None:
                tmp = self.color
                self.color = color
            x, y, w, h = rects
            ret = render.SDL_RenderFillRect(self.sdlrenderer, SDL_Rect(x, y, w, h))
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()
        else:
            x = 0
            rlist = (SDL_Rect * len(rects))()
            for idx, r in enumerate(rects):
                rlist[idx] = SDL_Rect(r[0], r[1], r[2], r[3])
            if color is not None:
                tmp = self.color
                self.color = color
            ptr = cast(rlist, POINTER(SDL_Rect))
            ret = render.SDL_RenderFillRects(self.sdlrenderer, ptr, len(rects))
            if color is not None:
                self.color = tmp
            if ret == -1:
                raise SDLError()