"""OS-specific font detection."""
import os
import sys
from subprocess import Popen, PIPE
from .compat import ISPYTHON2, stringify

if sys.platform in ("win32", "cli"):
    if ISPYTHON2:
        import _winreg as winreg
    else:
        import winreg

__all__ = ["STYLE_NORMAL", "STYLE_BOLD", "STYLE_ITALIC",
           "init", "list_fonts", "get_fonts", "get_font"
           ]

# Font cache entries:
# { family : [...,
#             (name, styles, fonttype, filename)
#             ...
#            ]
# }
__FONTCACHE = None


STYLE_NORMAL = 0x00
STYLE_BOLD =   0x01
STYLE_ITALIC = 0x02


def _add_font(family, name, styles, fonttype, filename):
    """Adds a font to the internal font cache."""
    global __FONTCACHE

    if family not in __FONTCACHE:
        __FONTCACHE[family] = []
    __FONTCACHE[family].append((name, styles, fonttype, filename))


def _cache_fonts_win32():
    """Caches fonts on a Win32 platform."""
    key = "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts"
    regfonts = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key) as fontkey:
            idx = 0
            enumval = winreg.EnumValue
            rappend = regfonts.append
            while True:
                rappend(enumval(fontkey, idx)[:2])
                idx += 1
    except WindowsError:
        pass

    # TODO: integrate alias handling for fonts within the registry.
    # TODO: Scan and index fonts from %SystemRoot%\\Fonts that are not in the
    # registry

    # Received all fonts from the registry.
    for name, filename in regfonts:
        fonttype = os.path.splitext(filename)[1][1:].lower()
        if name.endswith("(TrueType)"):
            name = name[:-10].strip()
        if name.endswith("(All Res)"):
            name = name[:-9].strip()
        style = STYLE_NORMAL
        if name.find(" Bold") >= 0:
            style |= STYLE_BOLD
        if name.find(" Italic") >= 0 or name.find(" Oblique") >= 0:
            style |= STYLE_ITALIC

        family = name
        for rm in ("Bold", "Italic", "Oblique"):
            family = family.replace(rm, "")
        family = family.lower().strip()

        fontpath = os.environ.get("SystemRoot", "C:\\Windows")
        fontpath = os.path.join(fontpath, "Fonts")
        if filename.find("\\") == -1:
            # No path delimiter is given; we assume it to be a font in
            # %SystemRoot%\Fonts
            filename = os.path.join(fontpath, filename)
        _add_font(family, name, style, fonttype, filename)


def _cache_fonts_darwin():
    """Caches fonts on Mac OS."""
    raise NotImplementedError("Mac OS X support is not given yet")


def _cache_fonts_fontconfig():
    """Caches font on POSIX-alike platforms."""
    try:
        command = "fc-list : file family style fullname fullnamelang"
        proc = Popen(command, stdout=PIPE, shell=True, stderr=PIPE)
        pout = proc.communicate()[0]
        output = stringify(pout, "utf-8")
    except OSError:
        return

    for entry in output.split(os.linesep):
        if entry.strip() == "":
            continue
        values = entry.split(":")
        filename = values[0]

        # get the font type
        fname, fonttype = os.path.splitext(filename)
        if fonttype == ".gz":
            fonttype = os.path.splitext(fname)[1][1:].lower()
        else:
            fonttype = fonttype.lstrip(".").lower()

        # get the font name
        name = None
        if len(values) > 3:
            fullnames, fullnamelangs = values[3:]
            langs = fullnamelangs.split(",")
            offset = langs.index("fullnamelang=en")
            if offset == -1:
                offset = langs.index("en")
            if offset != -1:
                # got an english name, use that one
                name = fullnames.split(",")[offset]
                if name.startswith("fullname="):
                    name = name[9:]
        if name is None:
            if fname.endswith(".pcf") or fname.endswith(".bdf"):
                name = os.path.basename(fname[:-4])
            else:
                name = os.path.basename(fname)
        name = name.lower()

        # family and styles
        family = values[1].strip().lower()
        stylevals = values[2].strip()
        style = STYLE_NORMAL

        if stylevals.find("Bold") >= 0:
            style |= STYLE_BOLD
        if stylevals.find("Italic") >= 0 or stylevals.find("Oblique") >= 0:
            style |= STYLE_ITALIC
        _add_font(family, name, style, fonttype, filename)


def init():
    """Initialises the internal font cache.

    It does not need to be called explicitly.
    """
    global __FONTCACHE
    if __FONTCACHE is not None:
        return
    __FONTCACHE = {}
    if sys.platform in ("win32", "cli"):
        _cache_fonts_win32()
    elif sys.platform == "darwin":
        _cache_fonts_darwin()
    else:
        _cache_fonts_fontconfig()


def list_fonts():
    """Returns an iterator over the cached fonts."""
    if __FONTCACHE is None:
        init()
    if len(__FONTCACHE) == 0:
        yield None
    for family, entries in __FONTCACHE.items():
        for fname, styles, fonttype, filename in entries:
            yield (family, fname, styles, fonttype, filename)


def get_fonts(name, style=STYLE_NORMAL, ftype=None):
    """Retrieves all fonts matching the given family or font name."""
    if __FONTCACHE is None:
        init()
    if len(__FONTCACHE) == 0:
        return None

    results = []
    rappend = results.append

    name = name.lower()
    if ftype:
        ftype = ftype.lower()

    fonts = __FONTCACHE.get(name, [])
    for fname, fstyles, fonttype, filename in fonts:
        if ftype and fonttype != ftype:
            # ignore font filetype mismatches
            continue
        if (fstyles & style) == style:
            rappend(filename)

    for family, fonts in __FONTCACHE.items():
        for fname, fstyles, fonttype, filename in fonts:
            if fname.lower() == name and filename not in results:
                rappend(filename)
    return results


def get_font(name, style=STYLE_NORMAL, ftype=None):
    """Retrieves the best matching font file for the given name and
    criteria.
    """
    retvals = get_fonts(name, style, ftype)
    if len(retvals) > 0:
        return retvals[0]
    return None
