import sys
import pytest
import copy
from sdl2.ext import color
from sdl2.ext.color import Color
from sdl2.ext.compat import *

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


class TestSDL2ExtColor(object):
    __tags__ = ["sdl2ext"]

    def test_Color(self):
        c = Color(10, 20, 30, 40)
        assert c.r == 10
        assert c.g == 20
        assert c.b == 30
        assert c.a == 40

        with pytest.raises(ValueError):
            Color(257, 10, 105, 44)
        with pytest.raises(ValueError):
            Color(10, 257, 105, 44)
        with pytest.raises(ValueError):
            Color(10, 105, 257, 44)
        with pytest.raises(ValueError):
            Color(10, 105, 44, 257)


    def test_Color__copy__(self):
        copy_copy = copy.copy
        for c in color_combos():
            c2 = copy_copy(c)
            assert c == c2
            c2 = ~c2
            assert c != c2


    def test_Color__eq__(self):
        assert Color(255, 0, 0, 0) == Color(255, 0, 0, 0)
        assert Color(0, 255, 0, 0) == Color(0, 255, 0, 0)
        assert Color(0, 0, 255, 0) == Color(0, 0, 255, 0)
        assert Color(0, 0, 0, 255) == Color(0, 0, 0, 255)

        assert not (Color(0, 0, 0, 0) == Color(255, 0, 0, 0))
        assert not (Color(0, 0, 0, 0) == Color(0, 255, 0, 0))
        assert not (Color(0, 0, 0, 0) == Color(0, 0, 255, 0))
        assert not (Color(0, 0, 0, 0) == Color(0, 0, 0, 255))

        assert tuple(Color(255, 0, 0, 0)) == (255, 0, 0, 0)
        assert tuple(Color(0, 255, 0, 0)) == (0, 255, 0, 0)
        assert tuple(Color(0, 0, 255, 0)) == (0, 0, 255, 0)
        assert tuple(Color(0, 0, 0, 255)) == (0, 0, 0, 255)

        assert not (tuple(Color(0, 0, 0, 0)) == (255, 0, 0, 0))
        assert not (tuple(Color(0, 0, 0, 0)) == (0, 255, 0, 0))
        assert not (tuple(Color(0, 0, 0, 0)) == (0, 0, 255, 0))
        assert not (tuple(Color(0, 0, 0, 0)) == (0, 0, 0, 255))

        assert int(Color(255, 0, 0, 0)) == 0xff000000
        assert int(Color(0, 255, 0, 0)) == 0x00ff0000
        assert int(Color(0, 0, 255, 0)) == 0x0000ff00
        assert int(Color(0, 0, 0, 255)) == 0x000000ff

        assert not (int(Color(0, 0, 0, 0)) == 0xff000000)
        assert not (int(Color(0, 0, 0, 0)) == 0x00ff0000)
        assert not (int(Color(0, 0, 0, 0)) == 0x0000ff00)
        assert not (int(Color(0, 0, 0, 0)) == 0x000000ff)


    def test_Color__ne__(self):
        assert Color(0, 0, 0, 0) != Color(255, 0, 0, 0)
        assert Color(0, 0, 0, 0) != Color(0, 255, 0, 0)
        assert Color(0, 0, 0, 0) != Color(0, 0, 255, 0)
        assert Color(0, 0, 0, 0) != Color(0, 0, 0, 255)

        assert not (Color(255, 0, 0, 0) != Color(255, 0, 0, 0))
        assert not (Color(0, 255, 0, 0) != Color(0, 255, 0, 0))
        assert not (Color(0, 0, 255, 0) != Color(0, 0, 255, 0))
        assert not (Color(0, 0, 0, 255) != Color(0, 0, 0, 255))

        assert tuple(Color(0, 0, 0, 0)) != (255, 0, 0, 0)
        assert tuple(Color(0, 0, 0, 0)) != (0, 255, 0, 0)
        assert tuple(Color(0, 0, 0, 0)) != (0, 0, 255, 0)
        assert tuple(Color(0, 0, 0, 0)) != (0, 0, 0, 255)

        assert not (tuple(Color(255, 0, 0, 0)) != (255, 0, 0, 0))
        assert not (tuple(Color(0, 255, 0, 0)) != (0, 255, 0, 0))
        assert not (tuple(Color(0, 0, 255, 0)) != (0, 0, 255, 0))
        assert not (tuple(Color(0, 0, 0, 255)) != (0, 0, 0, 255))

        assert int(Color(0, 0, 0, 0)) != 0xff000000
        assert int(Color(0, 0, 0, 0)) != 0x00ff0000
        assert int(Color(0, 0, 0, 0)) != 0x0000ff00
        assert int(Color(0, 0, 0, 0)) != 0x000000ff

        assert not (int(Color(255, 0, 0, 0)) != 0xff000000)
        assert not (int(Color(0, 255, 0, 0)) != 0x00ff0000)
        assert not (int(Color(0, 0, 255, 0)) != 0x0000ff00)
        assert not (int(Color(0, 0, 0, 255)) != 0x000000ff)


    def test_Color__repr__(self):
        c = Color(68, 38, 26, 69)
        c1 = eval(repr(c))
        assert c == c1


    def test_Color__int__(self):
        c = Color(0x00, 0xCC, 0x00, 0xCC)
        assert c.r == 0x00
        assert c.g == 0xCC
        assert c.b == 0x00
        assert c.a == 0xCC
        assert int(c) == int(0x00CC00CC)

        c = Color(0x72, 0x75, 0x92, 0x33)
        assert c.r == 0x72
        assert c.g == 0x75
        assert c.b == 0x92
        assert c.a == 0x33
        assert int(c) == int(0x72759233)


    def test_Color__long__(self):
        c = Color(0x00, 0xCC, 0x00, 0xCC)
        assert c.r == 0x00
        assert c.g == 0xCC
        assert c.b == 0x00
        assert c.a == 0xCC
        assert long(c) == long(0x00CC00CC)

        c = Color(0x72, 0x75, 0x92, 0x33)
        assert c.r == 0x72
        assert c.g == 0x75
        assert c.b == 0x92
        assert c.a == 0x33
        assert long(c) == long(0x72759233)


    def test_Color__float__(self):
        c = Color(0x00, 0xCC, 0x00, 0xCC)
        assert c.r == 0x00
        assert c.g == 0xCC
        assert c.b == 0x00
        assert c.a == 0xCC
        assert float(c) == float(0x00CC00CC)

        c = Color(0x72, 0x75, 0x92, 0x33)
        assert c.r == 0x72
        assert c.g == 0x75
        assert c.b == 0x92
        assert c.a == 0x33
        assert float(c) == float(0x72759233)


    def test_Color__oct__(self):
        c = Color(0x00, 0xCC, 0x00, 0xCC)
        assert c.r == 0x00
        assert c.g == 0xCC
        assert c.b == 0x00
        assert c.a == 0xCC
        assert oct(c) == oct(0x00CC00CC)

        c = Color(0x72, 0x75, 0x92, 0x33)
        assert c.r == 0x72
        assert c.g == 0x75
        assert c.b == 0x92
        assert c.a == 0x33
        assert oct(c) == oct(0x72759233)


    def test_Color__hex__(self):
        c = Color(0x00, 0xCC, 0x00, 0xCC)
        assert c.r == 0x00
        assert c.g == 0xCC
        assert c.b == 0x00
        assert c.a == 0xCC
        assert hex(c) == hex(0x00CC00CC)

        c = Color(0x72, 0x75, 0x92, 0x33)
        assert c.r == 0x72
        assert c.g == 0x75
        assert c.b == 0x92
        assert c.a == 0x33
        assert hex(c) == hex(0x72759233)


    def test_Color__invert__(self):
        assert ~Color() == Color(0, 0, 0, 0)
        assert ~Color(0, 0, 0, 0) == Color(255, 255, 255, 255)
        assert ~Color(255, 0, 0, 0) == Color(0, 255, 255, 255)
        assert ~Color(0, 255, 0, 0) == Color(255, 0, 255, 255)
        assert ~Color(0, 0, 255, 0) == Color(255, 255, 0, 255)
        assert ~Color(0, 0, 0, 255) == Color(255, 255, 255, 0)
        assert ~Color(127, 127, 127, 0) == Color(128, 128, 128, 255)

        assert ~Color(1, 2, 3, 4) == Color(254, 253, 252, 251)
        assert ~Color(127, 127, 127, 0) == Color(128, 128, 128, 255)


    def test_Color__mod__(self):
        c1 = Color()
        assert c1.r == 255
        assert c1.g == 255
        assert c1.b == 255
        assert c1.a == 255

        c2 = Color(2, 4, 8, 16)
        assert c2.r == 2
        assert c2.g == 4
        assert c2.b == 8
        assert c2.a == 16

        c3 = c1 % c2
        assert c3.r == 1
        assert c3.g == 3
        assert c3.b == 7
        assert c3.a == 15


    def test_Color__div__(self):
        c1 = Color(128, 128, 128, 128)
        assert c1.r == 128
        assert c1.g == 128
        assert c1.b == 128
        assert c1.a == 128

        c2 = Color(2, 4, 8, 16)
        assert c2.r == 2
        assert c2.g == 4
        assert c2.b == 8
        assert c2.a == 16

        c3 = c1 / c2
        assert c3.r == 64
        assert c3.g == 32
        assert c3.b == 16
        assert c3.a == 8

        c3 = c3 / c2
        assert c3.r == 32
        assert c3.g == 8
        assert c3.b == 2
        assert c3.a == 0


    def test_Color__mul__(self):
        c1 = Color(1, 1, 1, 1)
        assert c1.r == 1
        assert c1.g == 1
        assert c1.b == 1
        assert c1.a == 1

        c2 = Color(2, 5, 3, 22)
        assert c2.r == 2
        assert c2.g == 5
        assert c2.b == 3
        assert c2.a == 22

        c3 = c1 * c2
        assert c3.r == 2
        assert c3.g == 5
        assert c3.b == 3
        assert c3.a == 22

        c3 = c3 * c2
        assert c3.r == 4
        assert c3.g == 25
        assert c3.b == 9
        assert c3.a == 255


    def test_Color__sub__(self):
        c1 = Color(255, 255, 255, 255)
        assert c1.r == 255
        assert c1.g == 255
        assert c1.b == 255
        assert c1.a == 255

        c2 = Color(20, 33, 82, 193)
        assert c2.r == 20
        assert c2.g == 33
        assert c2.b == 82
        assert c2.a == 193

        c3 = c1 - c2
        assert c3.r == 235
        assert c3.g == 222
        assert c3.b == 173
        assert c3.a == 62

        c3 = c3 - c2
        assert c3.r == 215
        assert c3.g == 189
        assert c3.b == 91
        assert c3.a == 0


    def test_Color__add__(self):
        c1 = Color(0, 0, 0, 0)
        assert c1.r == 0
        assert c1.g == 0
        assert c1.b == 0
        assert c1.a == 0

        c2 = Color(20, 33, 82, 193)
        assert c2.r == 20
        assert c2.g == 33
        assert c2.b == 82
        assert c2.a == 193

        c3 = c1 + c2
        assert c3.r == 20
        assert c3.g == 33
        assert c3.b == 82
        assert c3.a == 193

        c3 = c3 + c2
        assert c3.r == 40
        assert c3.g == 66
        assert c3.b == 164
        assert c3.a == 255


    def test_Color__len__(self):
        c = Color(204, 38, 194, 55)
        assert len(c) == 4
        assert len(Color()) == 4
        assert len(Color(2)) == 4


    def test_Color__getitem__(self):
        c = Color(204, 38, 194, 55)
        assert c[0] == 204
        assert c[1] == 38
        assert c[2] == 194
        assert c[3] == 55


    def test_Color__setitem(self):
        c = Color(204, 38, 194, 55)
        assert c[0] == 204
        assert c[1] == 38
        assert c[2] == 194
        assert c[3] == 55

        c[0] = 33
        assert c[0] == 33
        c[1] = 48
        assert c[1] == 48
        c[2] = 173
        assert c[2] == 173
        c[3] = 213
        assert c[3] == 213

        # Now try some 'invalid' ones
        with pytest.raises(ValueError):
            _assign_item(c, 1, -83)
        assert c[1] == 48
        with pytest.raises(TypeError):
            _assign_item(c, 2, "Hello")
        assert c[2] == 173


    def test_Color_r(self):
        c = Color(100, 100, 100)
        assert c.r == 100

        c = Color(100, 100, 100, 100)
        assert c.r == 100

        c = Color(100, 100, 100)
        assert c.r == 100
        c.r = 200
        assert c.r == 200
        c.r += 22
        assert c.r == 222


    def test_Color_g(self):
        c = Color(100, 100, 100)
        assert c.g == 100

        c = Color(100, 100, 100, 100)
        assert c.g == 100

        c = Color(100, 100, 100)
        assert c.g == 100
        c.g = 200
        assert c.g == 200
        c.g += 22
        assert c.g == 222


    def test_Color_b(self):
        c = Color(100, 100, 100)
        assert c.b == 100

        c = Color(100, 100, 100, 100)
        assert c.b == 100

        c = Color(100, 100, 100)
        assert c.b == 100
        c.b = 200
        assert c.b == 200
        c.b += 22
        assert c.b == 222


    def test_Color_a(self):
        c = Color(100, 100, 100)
        assert c.a == 255

        c = Color(100, 100, 100, 100)
        assert c.a == 100

        c = Color(100, 100, 100)
        assert c.a == 255
        c.a = 200
        assert c.a == 200
        c.a += 22
        assert c.a == 222


    def test_Color_rgba(self):
        c = Color(0)
        assert c.r == 0
        assert c.g == 255
        assert c.b == 255
        assert c.a == 255

        # Test simple assignments
        c.r = 123
        assert c.r == 123
        with pytest.raises(ValueError):
            _assignr(c, 537)
        assert c.r == 123
        with pytest.raises(ValueError):
            _assignr(c, -3)
        assert c.r == 123
        assert c.g == 255
        assert c.b == 255
        assert c.a == 255

        c.g = 55
        assert c.g == 55
        with pytest.raises(ValueError):
            _assigng(c, 348)
        assert c.g == 55
        with pytest.raises(ValueError):
            _assigng(c, -44)
        assert c.g == 55
        assert c.r == 123
        assert c.b == 255
        assert c.a == 255

        c.b = 77
        assert c.b == 77
        with pytest.raises(ValueError):
            _assignb(c, 256)
        assert c.b == 77
        with pytest.raises(ValueError):
            _assignb(c, -12)
        assert c.b == 77
        assert c.r == 123
        assert c.g == 55
        assert c.a == 255

        c.a = 251
        assert c.a == 251
        with pytest.raises(ValueError):
            _assigna(c, 312)
        assert c.a == 251
        with pytest.raises(ValueError):
            _assigna(c, -10)
        assert c.a == 251
        assert c.r == 123
        assert c.g == 55
        assert c.b == 77


    def test_Color_hsva(self):
        for c in color_combos():
            h, s, v, a = c.hsva
            assert 0 <= h <= 360
            assert 0 <= s <= 100
            assert 0 <= v <= 100
            assert 0 <= a <= 100

            for cx in [(0, 0, 0, 0), (255, 255, 255, 255)]:
                c2 = Color(*cx)
                assert tuple(c2) == cx

                c2.hsva = c.hsva
                err = "Failed for color '%s' and cx '%s': %s" % (c, cx, c2)
                assert abs(c2.r - c.r <= 1), err
                assert abs(c2.g - c.g <= 1), err
                assert abs(c2.b - c.b <= 1), err
                assert abs(c2.a - c.a <= 1), err


    def test_Color_hsla(self):
        for c in color_combos():
            h, s, l, a = c.hsla
            assert 0 <= h <= 360
            assert 0 <= s <= 100
            assert 0 <= l <= 100
            assert 0 <= a <= 100

            for cx in [(0, 0, 0, 0), (255, 255, 255, 255)]:
                c2 = Color(*cx)
                assert tuple(c2) == cx

                c2.hsla = c.hsla
                err = "Failed for color '%s' and cx '%s': %s" % (c, cx, c2)
                assert abs(c2.r - c.r <= 1), err
                assert abs(c2.g - c.g <= 1), err
                assert abs(c2.b - c.b <= 1), err
                assert abs(c2.a - c.a <= 1), err


    def test_Color_i1i2i3(self):
        for c in color_combos():
            i1, i2, i3 = c.i1i2i3
            assert 0 <= i1 <= 1
            assert -0.5 <= i2 <= 0.5
            assert -0.5 <= i3 <= 0.5

            for cx in [(0, 0, 0, 0), (255, 255, 255, 255)]:
                c2 = Color(*cx)
                assert tuple(c2) == cx

                c2.i1i2i3 = c.i1i2i3
                err = "Failed for color '%s' and cx '%s': %s" % (c, cx, c2)
                # I1I2I3 ignores the alpha channel, thus we won't check it
                assert abs(c2.r - c.r <= 1), err
                assert abs(c2.g - c.g <= 1), err
                assert abs(c2.b - c.b <= 1), err


    def test_Color_cmy(self):
        for val in color_combos():
            c, m, y = val.cmy
            assert 0 <= c <= 1
            assert 0 <= m <= 1
            assert 0 <= y <= 1

            for cx in [(0, 0, 0, 0), (255, 255, 255, 255)]:
                c2 = Color(*cx)
                assert tuple(c2) == cx

                c2.cmy = val.cmy
                err = "Failed for color '%s' and cx '%s': %s" % (c, cx, c2)
                # CMY ignores the alpha channel, thus we won't check it
                assert abs(c2.r - val.r <= 1), err
                assert abs(c2.g - val.g <= 1), err
                assert abs(c2.b - val.b <= 1), err


    def test_Color_normalize(self):
        c = Color(204, 38, 194, 55)
        assert c.r == 204
        assert c.g == 38
        assert c.b == 194
        assert c.a == 55

        t = c.normalize()

        assert round(abs(t[0]-0.800000), 5) == 0
        assert round(abs(t[1]-0.149016), 5) == 0
        assert round(abs(t[2]-0.760784), 5) == 0
        assert round(abs(t[3]-0.215686), 5) == 0

        c = Color(255, 255, 255, 255)
        assert c.normalize() == (1.0, 1.0, 1.0, 1.0)
        c = Color(0, 0, 0, 0)
        assert c.normalize() == (0.0, 0.0, 0.0, 0.0)
        c = Color(128, 128, 128, 128)
        t = c.normalize()
        for v in t:
            assert round(abs(v-0.5), 2) == 0

        c = Color(128, 255, 0, 52)
        t = c.normalize()
        assert round(abs(t[0]-0.5), 2) == 0
        assert t[1] == 1.0
        assert t[2] == 0.0
        # 52 / 255 ~= .20
        assert round(abs(t[3]-0.2), 2) == 0


    def test_is_rgb_color(self):
        for v in color_combos():
            assert color.is_rgba_color(v)

        for v in rgba_combos():
            assert not color.is_rgba_color(v)
        for v in argb_combos():
            assert not color.is_rgba_color(v)
        for v in hex_combos():
            assert not color.is_rgba_color(v)
        for v in hash_combos():
            assert not color.is_rgba_color(v)


    def test_is_rgba_color(self):
        for v in color_combos():
            assert color.is_rgba_color(v)

        for v in rgba_combos():
            assert not color.is_rgba_color(v)
        for v in argb_combos():
            assert not color.is_rgba_color(v)
        for v in hex_combos():
            assert not color.is_rgba_color(v)
        for v in hash_combos():
            assert not color.is_rgba_color(v)


    def test_rgba_argb_to_color(self):

        assert color.RGBA == color.rgba_to_color
        assert color.ARGB == color.argb_to_color

        cvals = list(color_combos())
        for index, val in enumerate(rgba_combos()):
            c = cvals[index]
            if c.r == c.g == c.b == c.a:
                assert color.RGBA(val) == c
                assert color.ARGB(val) == c
                continue

            assert color.RGBA(val) == c, "Failed for '%s'" % val
            assert not color.ARGB(val) == c, "Failed for '0x%.8x'" % val

        for index, val in enumerate(argb_combos()):
            c = cvals[index]
            if c.r == c.g == c.b == c.a:
                assert color.RGBA(val) == c
                assert color.ARGB(val) == c
                continue

            assert color.ARGB(val) == c, "Failed for '%s'" % val
            assert not color.RGBA(val) == c, "Failed for '0x%.8x'" % val


    def test_string_to_color(self):
        for method in (color.string_to_color, color.convert_to_color,
                       color.COLOR):
            assert method('#00000000').r == 0x00
            assert method('#10000000').r == 0x10
            assert method('#20000000').r == 0x20
            assert method('#30000000').r == 0x30
            assert method('#40000000').r == 0x40
            assert method('#50000000').r == 0x50
            assert method('#60000000').r == 0x60
            assert method('#70000000').r == 0x70
            assert method('#80000000').r == 0x80
            assert method('#90000000').r == 0x90
            assert method('#A0000000').r == 0xA0
            assert method('#B0000000').r == 0xB0
            assert method('#C0000000').r == 0xC0
            assert method('#D0000000').r == 0xD0
            assert method('#E0000000').r == 0xE0
            assert method('#F0000000').r == 0xF0
            assert method('#01000000').r == 0x01
            assert method('#02000000').r == 0x02
            assert method('#03000000').r == 0x03
            assert method('#04000000').r == 0x04
            assert method('#05000000').r == 0x05
            assert method('#06000000').r == 0x06
            assert method('#07000000').r == 0x07
            assert method('#08000000').r == 0x08
            assert method('#09000000').r == 0x09
            assert method('#0A000000').r == 0x0A
            assert method('#0B000000').r == 0x0B
            assert method('#0C000000').r == 0x0C
            assert method('#0D000000').r == 0x0D
            assert method('#0E000000').r == 0x0E
            assert method('#0F000000').r == 0x0F

            with pytest.raises(ValueError):
                method("0x12345")
            with pytest.raises(ValueError):
                method("0x1234567")
            with pytest.raises(ValueError):
                method("#123456789")
            with pytest.raises(ValueError):
                method("#12345")
            with pytest.raises(ValueError):
                method("#1234567")
            with pytest.raises(ValueError):
                method("#123456789")

            with pytest.raises(ValueError):
                method("# f000000")
            with pytest.raises(ValueError):
                method("#f 000000")
            with pytest.raises(ValueError):
                method("#-f000000")
            with pytest.raises(ValueError):
                method("-#f000000")

            with pytest.raises(ValueError):
                method("0x f000000")
            with pytest.raises(ValueError):
                method("0xf 000000")
            with pytest.raises(ValueError):
                method("0x-f000000")
            with pytest.raises(ValueError):
                method("-0xf000000")

            with pytest.raises(ValueError):
                method("#cc00qq")
            with pytest.raises(ValueError):
                method("0xcc00qq")
            with pytest.raises(ValueError):
                method("09abcdef")
            with pytest.raises(ValueError):
                method("09abcde")
            with pytest.raises(ValueError):
                method("quarky")

            cvals = list(color_combos())
            for index, val in enumerate(hex_combos()):
                assert method(val) == cvals[index], "Failed for '%s'" % val
            for index, val in enumerate(hash_combos()):
                assert method(val) == cvals[index], "Failed for '%s'" % val

        with pytest.raises(TypeError):
            color.string_to_color(0xff000000)
        with pytest.raises(TypeError):
            color.string_to_color(Color())


    def test_convert_to_color(self):
        assert color.COLOR == color.convert_to_color
        cvals = list(color_combos())

        for index, val in enumerate(hex_combos()):
            assert color.COLOR(val) == cvals[index], "Failed for '%s'" % val

        for index, val in enumerate(hash_combos()):
            assert color.COLOR(val) == cvals[index], "Failed for '%s'" % val

        for index, val in enumerate(hex_combos()):
            assert color.COLOR(val) == cvals[index], "Failed for '%s'" % val

        for index, val in enumerate(argb_combos()):
            assert color.COLOR(val) == cvals[index], "Failed for '0x%.8x'" % val

        for index, val in enumerate(color_combos()):
            assert color.COLOR(val) == cvals[index], "Failed for '%s'" % val

        with pytest.raises(ValueError):
            color.convert_to_color(self)

        with pytest.raises(ValueError):
            color.convert_to_color("Test")
