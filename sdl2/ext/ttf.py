import os
from .. import surface, pixels
from .common import SDLError, raise_sdl_err
from .compat import *
from .color import Color, convert_to_color
from .draw import prepare_color
from .resources import _validate_path

_HASSDLTTF = True
try:
    from .. import sdlttf
except ImportError:
    _HASSDLTTF = False

__all__ = ["FontManager"]


def _ttf_init():
    if not _HASSDLTTF:
        raise RuntimeError("SDL_ttf is required, but is not installed.")

    # Check if TTF already initialized, return immediately if it was
    if sdlttf.TTF_WasInit > 0:
        return

    # Handle a weirdness in how TTF_Init and TTF_Quit work: TTF_Init
    # blindly increments TTF_WasInit every time it's called and TTF_Quit
    # blindly decrements it, but TTF_Quit only *actually* quits when 
    # TTF_WasInit - 1 == 0. Here, we try to ensure we're starting at 0.
    while sdlttf.TTF_WasInit() < 1:
        ret = sdlttf.TTF_Init()
        if ret != 0:
            raise_sdl_err("initializing the SDL_ttf library")


def _ttf_quit():
    if not _HASSDLTTF:
        raise RuntimeError("SDL_ttf is required, but is not installed.")

    # Make sure WasInit is non-negative before trying to quit
    while sdlttf.TTF_WasInit() < 1:
        ret = sdlttf.TTF_Init()
        if ret != 0:
            raise_sdl_err("initializing the SDL_ttf library")

    # Actually quit the library (won't really quit until TTF_WasInit == 0)
    while sdlttf.TTF_WasInit > 0:
        sdlttf.TTF_Quit()



class FontManager(object):
    """A class for managing and rendering TrueType fonts.
    
    This class provides a basic wrapper around the SDL_ttf library.

    One font path must be given to initialise the FontManager.
    :attr:`default_font` will be set to this font. *size* is the default
    font size in pixels. *color* and *bg_color* will give the FontManager
    a default color. *index* will select a specific font face from a file
    containing multiple font faces.
    
    The first face is always at index 0. It can be used for TTC (TrueType Font
    Collection) fonts.

    Attributes:
        size (int): The default font size in pt.

    """
    def __init__(self, font_path, alias=None, size=16,
                 color=Color(255, 255, 255), bg_color=Color(0, 0, 0), index=0):
        _ttf_init()
        self.fonts = {}  # fonts = {alias: {size:font_ptr}}
        self.aliases = {}  # aliases = {alias:font_path}
        self._textcolor = pixels.SDL_Color(0, 0, 0)
        self._bgcolor = pixels.SDL_Color(255, 255, 255)
        self.color = color
        self.bg_color = bg_color
        self.size = size
        self._default_font = self.add(font_path, alias, size, index)

    def __del__(self):
        """Close all opened fonts."""
        self.close()

    def close(self):
        """Closes all fonts opened by the class."""
        for alias, fonts in self.fonts.items():
            for size, font in fonts.items():
                if font:
                    sdlttf.TTF_CloseFont(font)
        self.fonts = {}
        self.aliases = {}

    def add(self, font_path, alias=None, size=None, index=0):
        """Adds a font to the :class:`FontManager`.
        
        *alias* is by default the font name, any other name can be passed,
        *size* is the font size in pixels and defaults to :attr:`size`.
        *index* selects a specific font face from a TTC (TrueType Font
        Collection) file. Returns the font pointer stored in :attr:`fonts`.

        """
        size = size or self.size
        if alias is None:
            # If no alias given, take the font name as alias
            basename = os.path.basename(font_path)
            alias = os.path.splitext(basename)[0]
            if alias in self.fonts:
                if size in self.fonts[alias] and self.fonts[alias]:
                    # font with selected size already opened
                    return
                else:
                    self._change_font_size(alias, size)
                    return
            else:
                if not os.path.isfile(font_path):
                    raise IOError("Cannot find %s" % font_path)

        font = self._load_font(font_path, size, index)
        self.aliases[alias] = font_path
        self.fonts[alias] = {}
        self.fonts[alias][size] = font
        return font

    def _load_font(self, font_path, size, index=0):
        """Helper function to open the font.

        Raises an exception if something went wrong.
        """
        fullpath, fname = _validate_path(font_path, "a font")
        fullpath = byteify(fullpath)
        font = sdlttf.TTF_OpenFontIndex(fullpath, size, index)
        if not font:
            raise_sdl_err("opening the font '{0}'".format(fname))
        return font

    def _change_font_size(self, alias, size):
        """Loads an already opened font in another size."""
        if alias not in self.fonts:
            raise KeyError("Font %s not loaded in FontManager" % alias)
        font = self._load_font(self.aliases[alias], size)
        self.fonts[alias][size] = font

    @property
    def color(self):
        """:obj:`~sdl2.ext.Color`: The color to use for rendering text."""
        c = self._textcolor
        return Color(c.r, c.g, c.b, c.a)

    @color.setter
    def color(self, value):
        c = convert_to_color(value)
        self._textcolor = pixels.SDL_Color(c.r, c.g, c.b, c.a)

    @property
    def bg_color(self):
        """:obj:`~sdl2.ext.Color`: The background color to use for rendering."""
        c = self._bgcolor
        return Color(c.r, c.g, c.b, c.a)

    @bg_color.setter
    def bg_color(self, value):
        c = convert_to_color(value)
        self._bgcolor = pixels.SDL_Color(c.r, c.g, c.b, c.a)

    @property
    def default_font(self):
        """str: The name of the default font. Must be set to the alias of a
        currently-loaded font.

        """
        for alias in self.fonts:
            for size, font in self.fonts[alias].items():
                if font == self._default_font:
                    return alias

    @default_font.setter
    def default_font(self, value):
        alias = value
        size = self.size
        if alias not in self.fonts:
            raise ValueError("Font %s not loaded in FontManager" % alias)
        # Check if size is already loaded, otherwise do it.
        if size not in self.fonts[alias]:
            self._change_font_size(alias, size)
            size = list(self.fonts[alias].keys())[0]
        self._default_font = self.fonts[alias][size]

    def render(self, text, alias=None, size=None, width=None, color=None,
               bg_color=None, **kwargs):
        """Renders text to a surface.

        Renders text to a surface. This method uses the font designated by
        the passed *alias* or, if *alias* is omitted, by the set
        :attr:`default_font`.  A *size* can be passed even if the font was
        not loaded with this size.  A *width* can be given for automatic line
        wrapping.  If no *bg_color* or *color* are given, it will default to
        the FontManager's :attr:`bg_color` and :attr:`color`.
    
        """
        alias = alias or self.default_font
        size = size or self.size
        if bg_color is None:
            bg_color = self._bgcolor
        elif not isinstance(bg_color, pixels.SDL_Color):
            c = convert_to_color(bg_color)
            bg_color = pixels.SDL_Color(c.r, c.g, c.b, c.a)
        if color is None:
            color = self._textcolor
        elif not isinstance(color, pixels.SDL_Color):
            c = convert_to_color(color)
            color = pixels.SDL_Color(c.r, c.g, c.b, c.a)
        if len(self.fonts) == 0:
            raise TypeError("There are no fonts selected.")
        font = self._default_font
        if alias not in self.aliases:
            raise KeyError("Font %s not loaded" % font)
        elif size not in self.fonts[alias]:
            self._change_font_size(alias, size)
        font = self.fonts[alias][size]
        text = byteify(text, "utf-8")
        if width:
            fontsf = sdlttf.TTF_RenderUTF8_Blended_Wrapped(font, text, color,
                                                           width)
            if not fontsf:
                raise SDLError(sdlttf.TTF_GetError())
            if bg_color != pixels.SDL_Color(0, 0, 0):
                fontsf = fontsf.contents
                w, h = fontsf.w, fontsf.h
                bpp = fontsf.format.contents.BitsPerPixel
                fmt = fontsf.format.contents.format
                bgsf = surface.SDL_CreateRGBSurfaceWithFormat(0, w, h, bpp, fmt)
                if not bgsf:
                    surface.SDL_FreeSurface(fontsf)
                    raise SDLError()
                bg_color = prepare_color(bg_color, bgsf.contents)
                surface.SDL_FillRect(bgsf, None, bg_color)
                surface.SDL_BlitSurface(fontsf, None, bgsf, None)
                return bgsf.contents
            return fontsf.contents
        sf = None
        if bg_color == pixels.SDL_Color(0, 0, 0):
            sf = sdlttf.TTF_RenderUTF8_Blended(font, text, color)
        else:
            sf = sdlttf.TTF_RenderUTF8_Shaded(font, text, color,
                                              bg_color)
        if not sf:
            raise SDLError(sdlttf.TTF_GetError())
        return sf.contents
