from .compat import isiterable
from .common import raise_sdl_err
from .color import convert_to_color
from .. import pixels
from .. import surface as surf
from ..rect import SDL_Rect

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
    elif isinstance(target, surf.SDL_Surface):
        rtarget = target
    elif "SDL_Surface" in str(type(target)):
        rtarget = target.contents
    else:
        raise TypeError(
            "{0} must be a valid Sprite or SDL Surface".format(argname)
        )
    return rtarget


def _create_surface(size, fill=None, fmt="ARGB8888", errname="SDL"):
    # Perform initial type and argument checking
    if not isiterable(size) and len(size) == 2:
        e = "Surface size must be a tuple of two positive integers."
        raise TypeError(e)
    if not all([i > 0 and int(i) == i for i in size]):
        e = "Surface height and width must both be positive integers (got {0})."
        raise ValueError(e.format(str(size)))
    if fmt not in pixels.NAME_MAP.keys() and fmt not in pixels.ALL_PIXELFORMATS:
        e = "'{0}' is not a supported SDL pixel format."
        raise ValueError(e.format(fmt))
    if fill is not None:
        fill = convert_to_color(fill)

    # Actually create a surface with the given pixel format
    w, h = size
    bpp = 32  # NOTE: according to the SDL_surface.c code, this has no effect
    fmt_enum = fmt if type(fmt) == int else pixels.NAME_MAP[fmt]
    sf = surf.SDL_CreateRGBSurfaceWithFormat(0, w, h, bpp, fmt_enum)
    if not sf:
        raise_sdl_err("creating the {0} surface".format(errname))

    # If provided, set the fill for the new surface
    if fill is not None:
        pixfmt = sf.contents.format.contents
        if pixfmt.Amask == 0:
            fill_col = pixels.SDL_MapRGB(pixfmt, fill.r, fill.g, fill.b)
        else:
            fill_col = pixels.SDL_MapRGBA(pixfmt, fill.r, fill.g, fill.b, fill.a)
        surf.SDL_FillRect(sf, None, fill_col)

    return sf


def subsurface(surface, area):
    """Creates a surface from a part of another surface.

    The two surfaces share pixel data. The subsurface *must not* be used after
    its parent has been freed!
    """
    surface_format = surface.format[0]
    subpixels = (surface.pixels + surface.pitch*area[1] +
                 surface_format.BytesPerPixel*area[0])
    return surf.SDL_CreateRGBSurfaceFrom(subpixels, area[2], area[3],
                                    surface_format.BitsPerPixel,
                                    surface.pitch, surface_format.Rmask,
                                    surface_format.Gmask, surface_format.Bmask,
                                    surface_format.Amask)[0]
