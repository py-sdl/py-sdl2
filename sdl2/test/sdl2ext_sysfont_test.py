import sys
import unittest
from ..ext import sysfont


class FontTest(unittest.TestCase):
    __tags__ = []

    def test_init(self):
        sysfont.init()

    def test_list_fonts(self):
        sansfonts = [f for f in sysfont.list_fonts() if "sans" in f[0]]
        self.assertGreaterEqual(len(sansfonts), 1)

    def test_get_fonts(self):
        fontnames = ["sans", "arial", "helvetica", "times new roman", "serif"]
        # At least two fonts must be found.
        success = 0
        for fname in fontnames:
            count = len(sysfont.get_fonts(fname))
            if count >= 1:
                success += 1
            count = len(sysfont.get_fonts(fname, sysfont.STYLE_BOLD))
            if count >= 1:
                success += 1
            count = len(sysfont.get_fonts(fname, sysfont.STYLE_ITALIC))
            if count >= 1:
                success += 1
            count = len(sysfont.get_fonts(fname, sysfont.STYLE_ITALIC |
                                          sysfont.STYLE_BOLD))
            if count >= 1:
                success += 1

        self.assertGreaterEqual(success, 4,
            "did not meet enough font criteria for get_fonts()")

    def test_get_font(self):
        fontnames = ["sans", "arial", "helvetica", "times new roman", "serif"]
        # At least two fonts must be found.
        success = 0
        for fname in fontnames:
            fontfile = sysfont.get_font(fname)
            if fontfile is not None:
                success += 1

        self.assertGreaterEqual(success, 2,
            "could not find the required fonts for get_font()")


if __name__ == '__main__':
    sys.exit(unittest.main())
