import sys
import unittest
import copy
from ..ext import color
from ..ext.color import Color
from ..ext.compat import *

combs = [0, 1, 2, 4, 8, 16, 32, 62, 63, 64, 126, 127, 128, 255]
all_combos = [(r, g, b, a) for r in combs
                           for g in combs
                           for b in combs
                           for a in combs]


def color_combos():
    for x in all_combos:
        yield Color(*x)


def hex_combos():
    for r, g, b, a in all_combos:
        yield "0x%.2x%.2x%.2x%.2x" % (r, g, b, a)


def hash_combos():
    for r, g, b, a in all_combos:
        yield "#%.2x%.2x%.2x%.2x" % (r, g, b, a)


def rgba_combos():
    for r, g, b, a in all_combos:
        yield (r << 24 | g << 16 | b << 8 | a)


def argb_combos():
    for r, g, b, a in all_combos:
        yield (a << 24 | r << 16 | g << 8 | b)


def _assignr(x, y):
    x.r = y


def _assigng(x, y):
    x.g = y


def _assignb(x, y):
    x.b = y


def _assigna(x, y):
    x.a = y


def _assign_item(x, p, y):
    x[p] = y


class SDL2ExtColorTest(unittest.TestCase):
    __tags__ = ["sdl2ext"]

    def test_Color(self):
        c = Color(10, 20, 30, 40)
        self.assertEqual(c.r, 10)
        self.assertEqual(c.g, 20)
        self.assertEqual(c.b, 30)
        self.assertEqual(c.a, 40)

        self.assertRaises(ValueError, Color, 257, 10, 105, 44)
        self.assertRaises(ValueError, Color, 10, 257, 105, 44)
        self.assertRaises(ValueError, Color, 10, 105, 257, 44)
        self.assertRaises(ValueError, Color, 10, 105, 44, 257)

    def test_Color__copy__(self):
        copy_copy = copy.copy
        assertEqual = self.assertEqual
        assertNotEqual = self.assertNotEqual
        for c in color_combos():
            c2 = copy_copy(c)
            assertEqual(c, c2)
            c2 = ~c2
            assertNotEqual(c, c2)

    def test_Color__eq__(self):
        self.assertTrue(Color(255, 0, 0, 0) == Color(255, 0, 0, 0))
        self.assertTrue(Color(0, 255, 0, 0) == Color(0, 255, 0, 0))
        self.assertTrue(Color(0, 0, 255, 0) == Color(0, 0, 255, 0))
        self.assertTrue(Color(0, 0, 0, 255) == Color(0, 0, 0, 255))

        self.assertFalse(Color(0, 0, 0, 0) == Color(255, 0, 0, 0))
        self.assertFalse(Color(0, 0, 0, 0) == Color(0, 255, 0, 0))
        self.assertFalse(Color(0, 0, 0, 0) == Color(0, 0, 255, 0))
        self.assertFalse(Color(0, 0, 0, 0) == Color(0, 0, 0, 255))

        self.assertTrue(tuple(Color(255, 0, 0, 0)) == (255, 0, 0, 0))
        self.assertTrue(tuple(Color(0, 255, 0, 0)) == (0, 255, 0, 0))
        self.assertTrue(tuple(Color(0, 0, 255, 0)) == (0, 0, 255, 0))
        self.assertTrue(tuple(Color(0, 0, 0, 255)) == (0, 0, 0, 255))

        self.assertFalse(tuple(Color(0, 0, 0, 0)) == (255, 0, 0, 0))
        self.assertFalse(tuple(Color(0, 0, 0, 0)) == (0, 255, 0, 0))
        self.assertFalse(tuple(Color(0, 0, 0, 0)) == (0, 0, 255, 0))
        self.assertFalse(tuple(Color(0, 0, 0, 0)) == (0, 0, 0, 255))

        self.assertTrue(int(Color(255, 0, 0, 0)) == 0xff000000)
        self.assertTrue(int(Color(0, 255, 0, 0)) == 0x00ff0000)
        self.assertTrue(int(Color(0, 0, 255, 0)) == 0x0000ff00)
        self.assertTrue(int(Color(0, 0, 0, 255)) == 0x000000ff)

        self.assertFalse(int(Color(0, 0, 0, 0)) == 0xff000000)
        self.assertFalse(int(Color(0, 0, 0, 0)) == 0x00ff0000)
        self.assertFalse(int(Color(0, 0, 0, 0)) == 0x0000ff00)
        self.assertFalse(int(Color(0, 0, 0, 0)) == 0x000000ff)

    def test_Color__ne__(self):
        self.assertTrue(Color(0, 0, 0, 0) != Color(255, 0, 0, 0))
        self.assertTrue(Color(0, 0, 0, 0) != Color(0, 255, 0, 0))
        self.assertTrue(Color(0, 0, 0, 0) != Color(0, 0, 255, 0))
        self.assertTrue(Color(0, 0, 0, 0) != Color(0, 0, 0, 255))

        self.assertFalse(Color(255, 0, 0, 0) != Color(255, 0, 0, 0))
        self.assertFalse(Color(0, 255, 0, 0) != Color(0, 255, 0, 0))
        self.assertFalse(Color(0, 0, 255, 0) != Color(0, 0, 255, 0))
        self.assertFalse(Color(0, 0, 0, 255) != Color(0, 0, 0, 255))

        self.assertTrue(tuple(Color(0, 0, 0, 0)) != (255, 0, 0, 0))
        self.assertTrue(tuple(Color(0, 0, 0, 0)) != (0, 255, 0, 0))
        self.assertTrue(tuple(Color(0, 0, 0, 0)) != (0, 0, 255, 0))
        self.assertTrue(tuple(Color(0, 0, 0, 0)) != (0, 0, 0, 255))

        self.assertFalse(tuple(Color(255, 0, 0, 0)) != (255, 0, 0, 0))
        self.assertFalse(tuple(Color(0, 255, 0, 0)) != (0, 255, 0, 0))
        self.assertFalse(tuple(Color(0, 0, 255, 0)) != (0, 0, 255, 0))
        self.assertFalse(tuple(Color(0, 0, 0, 255)) != (0, 0, 0, 255))

        self.assertTrue(int(Color(0, 0, 0, 0)) != 0xff000000)
        self.assertTrue(int(Color(0, 0, 0, 0)) != 0x00ff0000)
        self.assertTrue(int(Color(0, 0, 0, 0)) != 0x0000ff00)
        self.assertTrue(int(Color(0, 0, 0, 0)) != 0x000000ff)

        self.assertFalse(int(Color(255, 0, 0, 0)) != 0xff000000)
        self.assertFalse(int(Color(0, 255, 0, 0)) != 0x00ff0000)
        self.assertFalse(int(Color(0, 0, 255, 0)) != 0x0000ff00)
        self.assertFalse(int(Color(0, 0, 0, 255)) != 0x000000ff)

    def test_Color__repr__(self):
        c = Color(68, 38, 26, 69)
        c1 = eval(repr(c))
        self.assertEqual(c, c1)

    def test_Color__int__(self):
        c = Color(0x00, 0xCC, 0x00, 0xCC)
        self.assertEqual(c.r, 0x00)
        self.assertEqual(c.g, 0xCC)
        self.assertEqual(c.b, 0x00)
        self.assertEqual(c.a, 0xCC)
        self.assertEqual(int(c), int(0x00CC00CC))

        c = Color(0x72, 0x75, 0x92, 0x33)
        self.assertEqual(c.r, 0x72)
        self.assertEqual(c.g, 0x75)
        self.assertEqual(c.b, 0x92)
        self.assertEqual(c.a, 0x33)
        self.assertEqual(int(c), int(0x72759233))

    def test_Color__long__(self):
        c = Color(0x00, 0xCC, 0x00, 0xCC)
        self.assertEqual(c.r, 0x00)
        self.assertEqual(c.g, 0xCC)
        self.assertEqual(c.b, 0x00)
        self.assertEqual(c.a, 0xCC)
        self.assertEqual(long(c), long(0x00CC00CC))

        c = Color(0x72, 0x75, 0x92, 0x33)
        self.assertEqual(c.r, 0x72)
        self.assertEqual(c.g, 0x75)
        self.assertEqual(c.b, 0x92)
        self.assertEqual(c.a, 0x33)
        self.assertEqual(long(c), long(0x72759233))

    def test_Color__float__(self):
        c = Color(0x00, 0xCC, 0x00, 0xCC)
        self.assertEqual(c.r, 0x00)
        self.assertEqual(c.g, 0xCC)
        self.assertEqual(c.b, 0x00)
        self.assertEqual(c.a, 0xCC)
        self.assertEqual(float(c), float(0x00CC00CC))

        c = Color(0x72, 0x75, 0x92, 0x33)
        self.assertEqual(c.r, 0x72)
        self.assertEqual(c.g, 0x75)
        self.assertEqual(c.b, 0x92)
        self.assertEqual(c.a, 0x33)
        self.assertEqual(float(c), float(0x72759233))

    def test_Color__oct__(self):
        c = Color(0x00, 0xCC, 0x00, 0xCC)
        self.assertEqual(c.r, 0x00)
        self.assertEqual(c.g, 0xCC)
        self.assertEqual(c.b, 0x00)
        self.assertEqual(c.a, 0xCC)
        self.assertEqual(oct(c), oct(0x00CC00CC))

        c = Color(0x72, 0x75, 0x92, 0x33)
        self.assertEqual(c.r, 0x72)
        self.assertEqual(c.g, 0x75)
        self.assertEqual(c.b, 0x92)
        self.assertEqual(c.a, 0x33)
        self.assertEqual(oct(c), oct(0x72759233))

    def test_Color__hex__(self):
        c = Color(0x00, 0xCC, 0x00, 0xCC)
        self.assertEqual(c.r, 0x00)
        self.assertEqual(c.g, 0xCC)
        self.assertEqual(c.b, 0x00)
        self.assertEqual(c.a, 0xCC)
        self.assertEqual(hex(c), hex(0x00CC00CC))

        c = Color(0x72, 0x75, 0x92, 0x33)
        self.assertEqual(c.r, 0x72)
        self.assertEqual(c.g, 0x75)
        self.assertEqual(c.b, 0x92)
        self.assertEqual(c.a, 0x33)
        self.assertEqual(hex(c), hex(0x72759233))

    def test_Color__invert__(self):
        self.assertEqual(~Color(), Color(0, 0, 0, 0))
        self.assertEqual(~Color(0, 0, 0, 0), Color(255, 255, 255, 255))
        self.assertEqual(~Color(255, 0, 0, 0), Color(0, 255, 255, 255))
        self.assertEqual(~Color(0, 255, 0, 0), Color(255, 0, 255, 255))
        self.assertEqual(~Color(0, 0, 255, 0), Color(255, 255, 0, 255))
        self.assertEqual(~Color(0, 0, 0, 255), Color(255, 255, 255, 0))
        self.assertEqual(~Color(127, 127, 127, 0), Color(128, 128, 128, 255))

        self.assertEqual(~Color(1, 2, 3, 4), Color(254, 253, 252, 251))
        self.assertEqual(~Color(127, 127, 127, 0), Color(128, 128, 128, 255))

    def test_Color__mod__(self):
        c1 = Color()
        self.assertEqual(c1.r, 255)
        self.assertEqual(c1.g, 255)
        self.assertEqual(c1.b, 255)
        self.assertEqual(c1.a, 255)

        c2 = Color(2, 4, 8, 16)
        self.assertEqual(c2.r, 2)
        self.assertEqual(c2.g, 4)
        self.assertEqual(c2.b, 8)
        self.assertEqual(c2.a, 16)

        c3 = c1 % c2
        self.assertEqual(c3.r, 1)
        self.assertEqual(c3.g, 3)
        self.assertEqual(c3.b, 7)
        self.assertEqual(c3.a, 15)

    def test_Color__div__(self):
        c1 = Color(128, 128, 128, 128)
        self.assertEqual(c1.r, 128)
        self.assertEqual(c1.g, 128)
        self.assertEqual(c1.b, 128)
        self.assertEqual(c1.a, 128)

        c2 = Color(2, 4, 8, 16)
        self.assertEqual(c2.r, 2)
        self.assertEqual(c2.g, 4)
        self.assertEqual(c2.b, 8)
        self.assertEqual(c2.a, 16)

        c3 = c1 / c2
        self.assertEqual(c3.r, 64)
        self.assertEqual(c3.g, 32)
        self.assertEqual(c3.b, 16)
        self.assertEqual(c3.a, 8)

        c3 = c3 / c2
        self.assertEqual(c3.r, 32)
        self.assertEqual(c3.g, 8)
        self.assertEqual(c3.b, 2)
        self.assertEqual(c3.a, 0)

    def test_Color__mul__(self):
        c1 = Color(1, 1, 1, 1)
        self.assertEqual(c1.r, 1)
        self.assertEqual(c1.g, 1)
        self.assertEqual(c1.b, 1)
        self.assertEqual(c1.a, 1)

        c2 = Color(2, 5, 3, 22)
        self.assertEqual(c2.r, 2)
        self.assertEqual(c2.g, 5)
        self.assertEqual(c2.b, 3)
        self.assertEqual(c2.a, 22)

        c3 = c1 * c2
        self.assertEqual(c3.r, 2)
        self.assertEqual(c3.g, 5)
        self.assertEqual(c3.b, 3)
        self.assertEqual(c3.a, 22)

        c3 = c3 * c2
        self.assertEqual(c3.r, 4)
        self.assertEqual(c3.g, 25)
        self.assertEqual(c3.b, 9)
        self.assertEqual(c3.a, 255)

    def test_Color__sub__(self):
        c1 = Color(255, 255, 255, 255)
        self.assertEqual(c1.r, 255)
        self.assertEqual(c1.g, 255)
        self.assertEqual(c1.b, 255)
        self.assertEqual(c1.a, 255)

        c2 = Color(20, 33, 82, 193)
        self.assertEqual(c2.r, 20)
        self.assertEqual(c2.g, 33)
        self.assertEqual(c2.b, 82)
        self.assertEqual(c2.a, 193)

        c3 = c1 - c2
        self.assertEqual(c3.r, 235)
        self.assertEqual(c3.g, 222)
        self.assertEqual(c3.b, 173)
        self.assertEqual(c3.a, 62)

        c3 = c3 - c2
        self.assertEqual(c3.r, 215)
        self.assertEqual(c3.g, 189)
        self.assertEqual(c3.b, 91)
        self.assertEqual(c3.a, 0)

    def test_Color__add__(self):
        c1 = Color(0, 0, 0, 0)
        self.assertEqual(c1.r, 0)
        self.assertEqual(c1.g, 0)
        self.assertEqual(c1.b, 0)
        self.assertEqual(c1.a, 0)

        c2 = Color(20, 33, 82, 193)
        self.assertEqual(c2.r, 20)
        self.assertEqual(c2.g, 33)
        self.assertEqual(c2.b, 82)
        self.assertEqual(c2.a, 193)

        c3 = c1 + c2
        self.assertEqual(c3.r, 20)
        self.assertEqual(c3.g, 33)
        self.assertEqual(c3.b, 82)
        self.assertEqual(c3.a, 193)

        c3 = c3 + c2
        self.assertEqual(c3.r, 40)
        self.assertEqual(c3.g, 66)
        self.assertEqual(c3.b, 164)
        self.assertEqual(c3.a, 255)

    def test_Color__len__(self):
        c = Color(204, 38, 194, 55)
        self.assertEqual(len(c), 4)
        self.assertEqual(len(Color()), 4)
        self.assertEqual(len(Color(2)), 4)

    def test_Color__getitem__(self):
        c = Color(204, 38, 194, 55)
        self.assertEqual(c[0], 204)
        self.assertEqual(c[1], 38)
        self.assertEqual(c[2], 194)
        self.assertEqual(c[3], 55)

    def test_Color__setitem(self):
        c = Color(204, 38, 194, 55)
        self.assertEqual(c[0], 204)
        self.assertEqual(c[1], 38)
        self.assertEqual(c[2], 194)
        self.assertEqual(c[3], 55)

        c[0] = 33
        self.assertEqual(c[0], 33)
        c[1] = 48
        self.assertEqual(c[1], 48)
        c[2] = 173
        self.assertEqual(c[2], 173)
        c[3] = 213
        self.assertEqual(c[3], 213)

        # Now try some 'invalid' ones
        self.assertRaises(ValueError, _assign_item, c, 1, -83)
        self.assertEqual(c[1], 48)
        self.assertRaises(TypeError, _assign_item, c, 2, "Hello")
        self.assertEqual(c[2], 173)

    def test_Color_r(self):
        c = Color(100, 100, 100)
        self.assertEqual(c.r, 100)

        c = Color(100, 100, 100, 100)
        self.assertEqual(c.r, 100)

        c = Color(100, 100, 100)
        self.assertEqual(c.r, 100)
        c.r = 200
        self.assertEqual(c.r, 200)
        c.r += 22
        self.assertEqual(c.r, 222)

    def test_Color_g(self):
        c = Color(100, 100, 100)
        self.assertEqual(c.g, 100)

        c = Color(100, 100, 100, 100)
        self.assertEqual(c.g, 100)

        c = Color(100, 100, 100)
        self.assertEqual(c.g, 100)
        c.g = 200
        self.assertEqual(c.g, 200)
        c.g += 22
        self.assertEqual(c.g, 222)

    def test_Color_b(self):
        c = Color(100, 100, 100)
        self.assertEqual(c.b, 100)

        c = Color(100, 100, 100, 100)
        self.assertEqual(c.b, 100)

        c = Color(100, 100, 100)
        self.assertEqual(c.b, 100)
        c.b = 200
        self.assertEqual(c.b, 200)
        c.b += 22
        self.assertEqual(c.b, 222)

    def test_Color_a(self):
        c = Color(100, 100, 100)
        self.assertEqual(c.a, 255)

        c = Color(100, 100, 100, 100)
        self.assertEqual(c.a, 100)

        c = Color(100, 100, 100)
        self.assertEqual(c.a, 255)
        c.a = 200
        self.assertEqual(c.a, 200)
        c.a += 22
        self.assertEqual(c.a, 222)

    def test_Color_rgba(self):
        c = Color(0)
        self.assertEqual(c.r, 0)
        self.assertEqual(c.g, 255)
        self.assertEqual(c.b, 255)
        self.assertEqual(c.a, 255)

        # Test simple assignments
        c.r = 123
        self.assertEqual(c.r, 123)
        self.assertRaises(ValueError, _assignr, c, 537)
        self.assertEqual(c.r, 123)
        self.assertRaises(ValueError, _assignr, c, -3)
        self.assertEqual(c.r, 123)
        self.assertEqual(c.g, 255)
        self.assertEqual(c.b, 255)
        self.assertEqual(c.a, 255)

        c.g = 55
        self.assertEqual(c.g, 55)
        self.assertRaises(ValueError, _assigng, c, 348)
        self.assertEqual(c.g, 55)
        self.assertRaises(ValueError, _assigng, c, -44)
        self.assertEqual(c.g, 55)
        self.assertEqual(c.r, 123)
        self.assertEqual(c.b, 255)
        self.assertEqual(c.a, 255)

        c.b = 77
        self.assertEqual(c.b, 77)
        self.assertRaises(ValueError, _assignb, c, 256)
        self.assertEqual(c.b, 77)
        self.assertRaises(ValueError, _assignb, c, -12)
        self.assertEqual(c.b, 77)
        self.assertEqual(c.r, 123)
        self.assertEqual(c.g, 55)
        self.assertEqual(c.a, 255)

        c.a = 251
        self.assertEqual(c.a, 251)
        self.assertRaises(ValueError, _assigna, c, 312)
        self.assertEqual(c.a, 251)
        self.assertRaises(ValueError, _assigna, c, -10)
        self.assertEqual(c.a, 251)
        self.assertEqual(c.r, 123)
        self.assertEqual(c.g, 55)
        self.assertEqual(c.b, 77)

    def test_Color_hsva(self):
        assertTrue = self.assertTrue
        assertEqual = self.assertEqual
        for c in color_combos():
            h, s, v, a = c.hsva
            assertTrue(0 <= h <= 360)
            assertTrue(0 <= s <= 100)
            assertTrue(0 <= v <= 100)
            assertTrue(0 <= a <= 100)

            for cx in [(0, 0, 0, 0), (255, 255, 255, 255)]:
                c2 = Color(*cx)
                assertEqual(tuple(c2), cx)

                c2.hsva = c.hsva
                assertTrue(abs(c2.r - c.r) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))
                assertTrue(abs(c2.g - c.g) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))
                assertTrue(abs(c2.b - c.b) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))
                assertTrue(abs(c2.a - c.a) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))

    def test_Color_hsla(self):
        assertTrue = self.assertTrue
        assertEqual = self.assertEqual
        for c in color_combos():
            h, s, l, a = c.hsla
            assertTrue(0 <= h <= 360)
            assertTrue(0 <= s <= 100)
            assertTrue(0 <= l <= 100)
            assertTrue(0 <= a <= 100)

            for cx in [(0, 0, 0, 0), (255, 255, 255, 255)]:
                c2 = Color(*cx)
                assertEqual(tuple(c2), cx)

                c2.hsla = c.hsla
                assertTrue(abs(c2.r - c.r) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))
                assertTrue(abs(c2.g - c.g) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))
                assertTrue(abs(c2.b - c.b) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))
                assertTrue(abs(c2.a - c.a) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))

    def test_Color_i1i2i3(self):
        assertTrue = self.assertTrue
        assertEqual = self.assertEqual
        for c in color_combos():
            i1, i2, i3 = c.i1i2i3
            assertTrue(0 <= i1 <= 1)
            assertTrue(-0.5 <= i2 <= 0.5)
            assertTrue(-0.5 <= i3 <= 0.5)

            for cx in [(0, 0, 0, 0), (255, 255, 255, 255)]:
                c2 = Color(*cx)
                assertEqual(tuple(c2), cx)

                c2.i1i2i3 = c.i1i2i3
                # I1I2I3 ignores the alpha channel, thus we won't check it
                assertTrue(abs(c2.r - c.r) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))
                assertTrue(abs(c2.g - c.g) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))
                assertTrue(abs(c2.b - c.b) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (c, cx, c2))

    def test_Color_cmy(self):
        assertTrue = self.assertTrue
        assertEqual = self.assertEqual
        for val in color_combos():
            c, m, y = val.cmy
            assertTrue(0 <= c <= 1)
            assertTrue(0 <= m <= 1)
            assertTrue(0 <= y <= 1)

            for cx in [(0, 0, 0, 0), (255, 255, 255, 255)]:
                c2 = Color(*cx)
                assertEqual(tuple(c2), cx)

                c2.cmy = val.cmy
                # CMY ignores the alpha channel, thus we won't check it
                assertTrue(abs(c2.r - val.r) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (val, cx, c2))
                assertTrue(abs(c2.g - val.g) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (val, cx, c2))
                assertTrue(abs(c2.b - val.b) <= 1,
                    "Failed for color '%s' and cx '%s': %s" % (val, cx, c2))

    def test_Color_normalize(self):
        c = Color(204, 38, 194, 55)
        self.assertEqual(c.r, 204)
        self.assertEqual(c.g, 38)
        self.assertEqual(c.b, 194)
        self.assertEqual(c.a, 55)

        t = c.normalize()

        self.assertAlmostEquals(t[0], 0.800000, places=5)
        self.assertAlmostEquals(t[1], 0.149016, places=5)
        self.assertAlmostEquals(t[2], 0.760784, places=5)
        self.assertAlmostEquals(t[3], 0.215686, places=5)

        c = Color(255, 255, 255, 255)
        self.assertEqual(c.normalize(), (1.0, 1.0, 1.0, 1.0))
        c = Color(0, 0, 0, 0)
        self.assertEqual(c.normalize(), (0.0, 0.0, 0.0, 0.0))
        c = Color(128, 128, 128, 128)
        t = c.normalize()
        for v in t:
            self.assertAlmostEquals(v, 0.5, places=2)

        c = Color(128, 255, 0, 52)
        t = c.normalize()
        self.assertAlmostEquals(t[0], 0.5, places=2)
        self.assertEqual(t[1], 1.0)
        self.assertEqual(t[2], 0.0)
        # 52 / 255 ~= .20
        self.assertAlmostEquals(t[3], 0.2, places=2)

    def test_is_rgb_color(self):
        assertTrue = self.assertTrue
        assertFalse = self.assertFalse
        for v in color_combos():
            assertTrue(color.is_rgba_color(v))

        for v in rgba_combos():
            assertFalse(color.is_rgba_color(v))
        for v in argb_combos():
            assertFalse(color.is_rgba_color(v))
        for v in hex_combos():
            assertFalse(color.is_rgba_color(v))
        for v in hash_combos():
            assertFalse(color.is_rgba_color(v))

    def test_is_rgba_color(self):
        assertTrue = self.assertTrue
        assertFalse = self.assertFalse
        for v in color_combos():
            assertTrue(color.is_rgba_color(v))

        for v in rgba_combos():
            assertFalse(color.is_rgba_color(v))
        for v in argb_combos():
            assertFalse(color.is_rgba_color(v))
        for v in hex_combos():
            assertFalse(color.is_rgba_color(v))
        for v in hash_combos():
            assertFalse(color.is_rgba_color(v))

    def test_rgba_argb_to_color(self):
        self.assertEqual(color.RGBA, color.rgba_to_color)
        self.assertEqual(color.ARGB, color.argb_to_color)

        assertEqual = self.assertEqual
        assertNotEqual = self.assertNotEqual

        cvals = list(color_combos())
        for index, val in enumerate(rgba_combos()):
            c = cvals[index]
            if c.r == c.g == c.b == c.a:
                assertEqual(color.RGBA(val), c)
                assertEqual(color.ARGB(val), c)
                continue

            assertEqual(color.RGBA(val), c, "Failed for '%s'" % val)
            assertNotEqual(color.ARGB(val), c, "Failed for '0x%.8x'" % val)

        for index, val in enumerate(argb_combos()):
            c = cvals[index]
            if c.r == c.g == c.b == c.a:
                assertEqual(color.RGBA(val), c)
                assertEqual(color.ARGB(val), c)
                continue

            assertEqual(color.ARGB(val), c, "Failed for '%s'" % val)
            assertNotEqual(color.RGBA(val), c, "Failed for '0x%.8x'" % val)

    def test_string_to_color(self):
        assertEqual = self.assertEqual
        assertRaises = self.assertRaises
        for method in(color.string_to_color, color.convert_to_color,
                      color.COLOR):
            assertEqual(method('#00000000').r, 0x00)
            assertEqual(method('#10000000').r, 0x10)
            assertEqual(method('#20000000').r, 0x20)
            assertEqual(method('#30000000').r, 0x30)
            assertEqual(method('#40000000').r, 0x40)
            assertEqual(method('#50000000').r, 0x50)
            assertEqual(method('#60000000').r, 0x60)
            assertEqual(method('#70000000').r, 0x70)
            assertEqual(method('#80000000').r, 0x80)
            assertEqual(method('#90000000').r, 0x90)
            assertEqual(method('#A0000000').r, 0xA0)
            assertEqual(method('#B0000000').r, 0xB0)
            assertEqual(method('#C0000000').r, 0xC0)
            assertEqual(method('#D0000000').r, 0xD0)
            assertEqual(method('#E0000000').r, 0xE0)
            assertEqual(method('#F0000000').r, 0xF0)
            assertEqual(method('#01000000').r, 0x01)
            assertEqual(method('#02000000').r, 0x02)
            assertEqual(method('#03000000').r, 0x03)
            assertEqual(method('#04000000').r, 0x04)
            assertEqual(method('#05000000').r, 0x05)
            assertEqual(method('#06000000').r, 0x06)
            assertEqual(method('#07000000').r, 0x07)
            assertEqual(method('#08000000').r, 0x08)
            assertEqual(method('#09000000').r, 0x09)
            assertEqual(method('#0A000000').r, 0x0A)
            assertEqual(method('#0B000000').r, 0x0B)
            assertEqual(method('#0C000000').r, 0x0C)
            assertEqual(method('#0D000000').r, 0x0D)
            assertEqual(method('#0E000000').r, 0x0E)
            assertEqual(method('#0F000000').r, 0x0F)

            assertRaises(ValueError, method, "0x12345")
            assertRaises(ValueError, method, "0x1234567")
            assertRaises(ValueError, method, "#123456789")
            assertRaises(ValueError, method, "#12345")
            assertRaises(ValueError, method, "#1234567")
            assertRaises(ValueError, method, "#123456789")

            assertRaises(ValueError, method, "# f000000")
            assertRaises(ValueError, method, "#f 000000")
            assertRaises(ValueError, method, "#-f000000")
            assertRaises(ValueError, method, "-#f000000")

            assertRaises(ValueError, method, "0x f000000")
            assertRaises(ValueError, method, "0xf 000000")
            assertRaises(ValueError, method, "0x-f000000")
            assertRaises(ValueError, method, "-0xf000000")

            assertRaises(ValueError, method, "#cc00qq")
            assertRaises(ValueError, method, "0xcc00qq")
            assertRaises(ValueError, method, "09abcdef")
            assertRaises(ValueError, method, "09abcde")
            assertRaises(ValueError, method, "quarky")

            cvals = list(color_combos())
            for index, val in enumerate(hex_combos()):
                assertEqual(method(val), cvals[index], "Failed for '%s'" % val)
            for index, val in enumerate(hash_combos()):
                assertEqual(method(val), cvals[index], "Failed for '%s'" % val)

        self.assertRaises(TypeError, color.string_to_color, 0xff000000)
        self.assertRaises(TypeError, color.string_to_color, Color())

    def test_convert_to_color(self):
        self.assertEqual(color.COLOR, color.convert_to_color)
        cvals = list(color_combos())

        assertEqual = self.assertEqual
        for index, val in enumerate(hex_combos()):
            assertEqual(color.COLOR(val), cvals[index],
                        "Failed for '%s'" % val)

        for index, val in enumerate(hash_combos()):
            assertEqual(color.COLOR(val), cvals[index],
                        "Failed for '%s'" % val)

        for index, val in enumerate(hex_combos()):
            assertEqual(color.COLOR(val), cvals[index],
                        "Failed for '%s'" % val)

        for index, val in enumerate(argb_combos()):
            assertEqual(color.COLOR(val), cvals[index],
                        "Failed for '0x%.8x'" % val)

        for index, val in enumerate(color_combos()):
            assertEqual(color.COLOR(val), cvals[index],
                        "Failed for '%s'" % val)

        self.assertRaises(ValueError, color.convert_to_color, self)
        self.assertRaises(ValueError, color.convert_to_color, "Test")


if __name__ == '__main__':
    sys.exit(unittest.main())
