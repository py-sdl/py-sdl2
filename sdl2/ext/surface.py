from .compat import isiterable
from ..rect import SDL_Rect
from ..surface import SDL_CreateRGBSurfaceFrom, SDL_Surface

__all__ = ["subsurface"]


def _get_rect_tuple(r, argname):
    if isinstance(r, SDL_Rect):
        return (r.x, r.y, r.w, r.h)
    elif isiterable(r) and len(r) == 4:
        return tuple(r)
    else:
        e = "'{0}' must be an SDL_Rect or tuple of 4 integers."
        raise TypeError(e.format(argname))


def _get_target_surface(target, argname="target"):
    """Gets the SDL_surface from the passed target."""
    if hasattr(target, "surface"):  # i.e. if SoftwareSprite
        rtarget = target.surface  
    elif isinstance(target, SDL_Surface):
        rtarget = target
    elif "SDL_Surface" in str(type(target)):
        rtarget = target.contents
    else:
        raise TypeError(
            "{0} must be a valid Sprite or SDL Surface".format(argname)
        )
    return rtarget


def subsurface(surface, area):
    """Creates a new :obj:`~sdl2.SDL_Surface` from a part of another surface.

    Surfaces created with this function will share pixel data with the original
    surface, meaning that any modifications to one surface will result in
    modifications to the other.

    .. warning::
       Because subsurfaces share pixel data with their parent surface, they
       *cannot* be used after the parent surface is freed. Doing so will
       almost certainly result in a segfault.

    Args:
        surface (:obj:`~sdl2.SDL_Surface`): The parent surface from which
            new sub-surface should be created.
        area (:obj:`SDL_Rect`, tuple): The ``(x, y, w, h)`` subset of the parent
            surface to use for the new surface, where ``x, y`` are the pixel
            coordinates of the top-left corner of the rectangle and ``w, h`` are
            its width and height (in pixels). Can also be specified as an
            :obj:`SDL_Rect`.

    Returns:
        :obj:`~sdl2.SDL_Surface`: The newly-created subsurface.

    """
    if not isinstance(surface, SDL_Surface):
        if "SDL_Surface" in str(type(surface)):
            surface = surface.contents
        else:
            e = "'surface' must be an SDL_Surface (got {0})"
            raise TypeError(e.format(type(surface)))

    x, y, w, h = _get_rect_tuple(area, argname="area")
    if x + w > surface.w or y + h > surface.h:
        e = "The specified area {0} exceeds the bounds of the parent surface "
        e += str((surface.w, surface.h))
        raise ValueError(e.format(str(area)))

    fmt = surface.format[0]
    bpp = fmt.BitsPerPixel
    subpixels = (surface.pixels + surface.pitch * y + fmt.BytesPerPixel * x)
    new =  SDL_CreateRGBSurfaceFrom(
        subpixels, w, h, bpp, surface.pitch, fmt.Rmask, fmt.Gmask, fmt.Bmask, fmt.Amask
    )
    return new.contents
