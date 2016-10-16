import sys
import copy
import unittest
from ctypes import byref, c_int
from .. import rect

to_ctypes = lambda seq, dtype: (dtype * len(seq))(*seq)


class SDLRectTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def test_SDL_Point(self):
        pt = rect.SDL_Point()
        self.assertEqual((pt.x, pt.y), (0, 0))
        for x in range(-100, 100):
            for y in range(-100, 100):
                pt = rect.SDL_Point(x, y)
                self.assertEqual((pt.x, pt.y), (x, y))

    def test_SDL_Point_x(self):
        pt = rect.SDL_Point()

        def setx(point, val):
            point.x = val

        for x in range(-1000, 1000):
            pt.x = x
            self.assertEqual((pt.x, pt.y), (x, 0))

        self.assertRaises(TypeError, setx, pt, 10.4)
        self.assertRaises(TypeError, setx, pt, "Test")
        self.assertRaises(TypeError, setx, pt, None)

    def test_SDL_Point_y(self):
        pt = rect.SDL_Point()

        def sety(point, val):
            point.y = val

        for x in range(-1000, 1000):
            pt.y = x
            self.assertEqual((pt.x, pt.y), (0, x))

        self.assertRaises(TypeError, sety, pt, 10.4)
        self.assertRaises(TypeError, sety, pt, "Test")
        self.assertRaises(TypeError, sety, pt, None)

    def test_SDL_Point__repr__(self):
        pt = rect.SDL_Point()
        pt2 = eval("rect.%s" % repr(pt))
        self.assertEqual(pt, pt2)
        self.assertEqual((pt.x, pt.y), (pt2.x, pt2.y))

        pt = rect.SDL_Point(10, 12)
        pt2 = eval("rect.%s" % repr(pt))
        self.assertEqual(pt, pt2)
        self.assertEqual((pt.x, pt.y), (pt2.x, pt2.y))

    def test_SDL_Point__copy__(self):
        pt = rect.SDL_Point()
        pt2 = copy.copy(pt)
        self.assertEqual(pt, pt2)
        self.assertEqual((pt.x, pt.y), (pt2.x, pt2.y))

        pt2.x = 7
        pt2.y = 9

        pt3 = copy.copy(pt2)
        self.assertNotEqual(pt, pt2)
        self.assertEqual(pt3, pt2)

    def test_SDL_Point__eq__(self):
        self.assertTrue(rect.SDL_Point() == rect.SDL_Point())
        self.assertTrue(rect.SDL_Point(0, 0) == rect.SDL_Point(0, 0))
        self.assertTrue(rect.SDL_Point(10, 0) == rect.SDL_Point(10, 0))
        self.assertTrue(rect.SDL_Point(0, 10) == rect.SDL_Point(0, 10))
        self.assertTrue(rect.SDL_Point(12, 10) == rect.SDL_Point(12, 10))

        self.assertFalse(rect.SDL_Point(0, 0) == rect.SDL_Point(0, 1))
        self.assertFalse(rect.SDL_Point(0, 0) == rect.SDL_Point(1, 0))
        self.assertFalse(rect.SDL_Point(0, 0) == rect.SDL_Point(1, 1))

        self.assertFalse(rect.SDL_Point(10, 10) == rect.SDL_Point(10, 0))
        self.assertFalse(rect.SDL_Point(7, 10) == rect.SDL_Point(0, 10))
        self.assertFalse(rect.SDL_Point(12, 10) == rect.SDL_Point(12, 11))

    def test_SDL_Point__ne__(self):
        self.assertFalse(rect.SDL_Point() != rect.SDL_Point())
        self.assertFalse(rect.SDL_Point(0, 0) != rect.SDL_Point(0, 0))
        self.assertFalse(rect.SDL_Point(10, 0) != rect.SDL_Point(10, 0))
        self.assertFalse(rect.SDL_Point(0, 10) != rect.SDL_Point(0, 10))
        self.assertFalse(rect.SDL_Point(12, 10) != rect.SDL_Point(12, 10))

        self.assertTrue(rect.SDL_Point(0, 0) != rect.SDL_Point(0, 1))
        self.assertTrue(rect.SDL_Point(0, 0) != rect.SDL_Point(1, 0))
        self.assertTrue(rect.SDL_Point(0, 0) != rect.SDL_Point(1, 1))

        self.assertTrue(rect.SDL_Point(10, 10) != rect.SDL_Point(10, 0))
        self.assertTrue(rect.SDL_Point(7, 10) != rect.SDL_Point(0, 10))
        self.assertTrue(rect.SDL_Point(12, 10) != rect.SDL_Point(12, 11))

    def test_SDL_Rect(self):
        rt = rect.SDL_Rect()
        self.assertEqual((rt.x, rt.y, rt.w, rt.h), (0, 0, 0, 0))
        for x in range(-10, 10):
            for y in range(-10, 10):
                for w in range(-10, 10):
                    for h in range(-10, 10):
                        rt = rect.SDL_Rect(x, y, w, h)
                        self.assertEqual((rt.x, rt.y, rt.w, rt.h),
                                         (x, y, w, h))

    def test_SDL_Rect__repr__(self):
        rt = rect.SDL_Rect(1, 2, 3, 4)
        rt2 = eval("rect.%s" % repr(rt))
        self.assertEqual((rt.x, rt.y, rt.w, rt.h),
                         (rt2.x, rt2.y, rt2.w, rt2.h))
        self.assertEqual(rt, rt2)

    def test_SDL_Rect__copy__(self):
        rt = rect.SDL_Rect()
        rt2 = copy.copy(rt)
        self.assertEqual(rt, rt2)
        self.assertEqual((rt.x, rt.y, rt.w, rt.h),
                         (rt2.x, rt2.y, rt2.w, rt2.h))

        rt2.x = 5
        rt2.y = 33
        rt2.w = 17
        rt2.w = 212

        rt3 = copy.copy(rt2)
        self.assertNotEqual(rt, rt2)
        self.assertEqual(rt3, rt2)

    def test_SDL_Rect__eq__(self):
        sdlr = rect.SDL_Rect

        self.assertTrue(sdlr() == sdlr())
        self.assertTrue(sdlr(0, 0, 0, 0) == sdlr(0, 0, 0, 0))
        self.assertTrue(sdlr(1, 2, 3, 4) == sdlr(1, 2, 3, 4))
        self.assertTrue(sdlr(-1, -2, -3, -4) == sdlr(-1, -2, -3, -4))

        self.assertTrue(sdlr(10, 0, 0, 0) == sdlr(10, 0, 0, 0))
        self.assertTrue(sdlr(0, 10, 0, 0) == sdlr(0, 10, 0, 0))
        self.assertTrue(sdlr(0, 0, 10, 0) == sdlr(0, 0, 10, 0))
        self.assertTrue(sdlr(0, 0, 0, 10) == sdlr(0, 0, 0, 10))

        self.assertTrue(sdlr(10, 10, 0, 0) == sdlr(10, 10, 0, 0))
        self.assertTrue(sdlr(0, 10, 10, 0) == sdlr(0, 10, 10, 0))
        self.assertTrue(sdlr(0, 0, 10, 10) == sdlr(0, 0, 10, 10))
        self.assertTrue(sdlr(10, 0, 0, 10) == sdlr(10, 0, 0, 10))

        self.assertTrue(sdlr(10, 10, 10, 0) == sdlr(10, 10, 10, 0))
        self.assertTrue(sdlr(0, 10, 10, 10) == sdlr(0, 10, 10, 10))

        self.assertFalse(sdlr() == sdlr(0, 0, 0, 1))
        self.assertFalse(sdlr(10, 0, 0, 0) == sdlr(0, 0, 0, 0))
        self.assertFalse(sdlr(10, 10, 0, 0) == sdlr(0, 10, 0, 0))
        self.assertFalse(sdlr(10, 0, 10, 0) == sdlr(0, 0, 10, 0))
        self.assertFalse(sdlr(10, 0, 0, 10) == sdlr(0, 0, 0, 10))
        self.assertFalse(sdlr(1, 2, 3, 4) == sdlr(-1, -2, -3, -4))

    def test_SDL_Rect__ne__(self):
        sdlr = rect.SDL_Rect

        self.assertTrue(sdlr() != sdlr(0, 0, 0, 1))
        self.assertTrue(sdlr(10, 0, 0, 0) != sdlr(0, 0, 0, 0))
        self.assertTrue(sdlr(10, 10, 0, 0) != sdlr(0, 10, 0, 0))
        self.assertTrue(sdlr(10, 0, 10, 0) != sdlr(0, 0, 10, 0))
        self.assertTrue(sdlr(10, 0, 0, 10) != sdlr(0, 0, 0, 10))
        self.assertTrue(sdlr(1, 2, 3, 4) != sdlr(-1, -2, -3, -4))

        self.assertFalse(sdlr() != sdlr())
        self.assertFalse(sdlr(0, 0, 0, 0) != sdlr(0, 0, 0, 0))
        self.assertFalse(sdlr(1, 2, 3, 4) != sdlr(1, 2, 3, 4))
        self.assertFalse(sdlr(-1, -2, -3, -4) != sdlr(-1, -2, -3, -4))

        self.assertFalse(sdlr(10, 0, 0, 0) != sdlr(10, 0, 0, 0))
        self.assertFalse(sdlr(0, 10, 0, 0) != sdlr(0, 10, 0, 0))
        self.assertFalse(sdlr(0, 0, 10, 0) != sdlr(0, 0, 10, 0))
        self.assertFalse(sdlr(0, 0, 0, 10) != sdlr(0, 0, 0, 10))

        self.assertFalse(sdlr(10, 10, 0, 0) != sdlr(10, 10, 0, 0))
        self.assertFalse(sdlr(0, 10, 10, 0) != sdlr(0, 10, 10, 0))
        self.assertFalse(sdlr(0, 0, 10, 10) != sdlr(0, 0, 10, 10))
        self.assertFalse(sdlr(10, 0, 0, 10) != sdlr(10, 0, 0, 10))

        self.assertFalse(sdlr(10, 10, 10, 0) != sdlr(10, 10, 10, 0))
        self.assertFalse(sdlr(0, 10, 10, 10) != sdlr(0, 10, 10, 10))

    def test_SDL_Rect_x(self):
        rt = rect.SDL_Rect()

        def setx(r, val):
            r.x = val

        for x in range(-1000, 1000):
            rt.x = x
            self.assertEqual((rt.x, rt.y, rt.w, rt.h), (x, 0, 0, 0))

        self.assertRaises(TypeError, setx, rt, 10.4)
        self.assertRaises(TypeError, setx, rt, "Test")
        self.assertRaises(TypeError, setx, rt, None)

    def test_SDL_Rect_y(self):
        rt = rect.SDL_Rect()

        def sety(r, val):
            r.y = val

        for x in range(-1000, 1000):
            rt.y = x
            self.assertEqual((rt.x, rt.y, rt.w, rt.h), (0, x, 0, 0))

        self.assertRaises(TypeError, sety, rt, 10.4)
        self.assertRaises(TypeError, sety, rt, "Test")
        self.assertRaises(TypeError, sety, rt, None)

    def test_SDL_Rect_w(self):
        rt = rect.SDL_Rect()

        def setw(r, val):
            r.w = val

        for x in range(-1000, 1000):
            rt.w = x
            self.assertEqual((rt.x, rt.y, rt.w, rt.h), (0, 0, x, 0))

        self.assertRaises(TypeError, setw, rt, 10.4)
        self.assertRaises(TypeError, setw, rt, "Test")
        self.assertRaises(TypeError, setw, rt, None)

    def test_SDL_Rect_h(self):
        rt = rect.SDL_Rect()

        def seth(r, val):
            r.h = val

        for x in range(-1000, 1000):
            rt.h = x
            self.assertEqual((rt.x, rt.y, rt.w, rt.h), (0, 0, 0, x))

        self.assertRaises(TypeError, seth, rt, 10.4)
        self.assertRaises(TypeError, seth, rt, "Test")
        self.assertRaises(TypeError, seth, rt, None)

    def test_SDL_RectEmpty(self):
        for w in range(-100, 100):
            for h in range(-100, 100):
                r = rect.SDL_Rect(0, 0, w, h)
                if w > 0 and h > 0:
                    self.assertFalse(rect.SDL_RectEmpty(r))
                else:
                    self.assertTrue(rect.SDL_RectEmpty(r))
        self.assertRaises(AttributeError, rect.SDL_RectEmpty, "Test")

    def test_SDL_RectEquals(self):
        r1 = rect.SDL_Rect(0, 0, 0, 0)
        r2 = rect.SDL_Rect(0, 0, 0, 0)
        self.assertTrue(rect.SDL_RectEquals(r1, r2))
        self.assertEqual(r1, r2)
        r2 = rect.SDL_Rect(-1, 2, 0, 0)
        self.assertFalse(rect.SDL_RectEquals(r1, r2))
        self.assertNotEqual(r1, r2)
        r2 = rect.SDL_Rect(0, 0, 1, 2)
        self.assertFalse(rect.SDL_RectEquals(r1, r2))
        self.assertNotEqual(r1, r2)
        self.assertRaises(AttributeError, rect.SDL_RectEquals, "Test", r2)
        self.assertRaises(AttributeError, rect.SDL_RectEquals, r1, None)
        self.assertRaises(AttributeError, rect.SDL_RectEquals, r1, "Test")

    def test_SDL_UnionRect(self):
        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(20, 20, 10, 10)
        r3 = rect.SDL_Rect()
        rect.SDL_UnionRect(r1, r2, byref(r3))
        self.assertEqual((r3.x, r3.y, r3.w, r3.h), (0, 0, 30, 30))

        r1 = rect.SDL_Rect(0, 0, 0, 0)
        r2 = rect.SDL_Rect(20, 20, 10, 10)
        rect.SDL_UnionRect(r1, r2, byref(r3))
        self.assertEqual((r3.x, r3.y, r3.w, r3.h), (20, 20, 10, 10))

        r1 = rect.SDL_Rect(-200, -4, 450, 33)
        r2 = rect.SDL_Rect(20, 20, 10, 10)
        rect.SDL_UnionRect(r1, r2, byref(r3))
        self.assertEqual((r3.x, r3.y, r3.w, r3.h), (-200, -4, 450, 34))

        r1 = rect.SDL_Rect(0, 0, 15, 16)
        r2 = rect.SDL_Rect(20, 20, 0, 0)
        rect.SDL_UnionRect(r1, r2, byref(r3))
        self.assertEqual((r3.x, r3.y, r3.w, r3.h), (0, 0, 15, 16))

        self.assertRaises((AttributeError, TypeError),
                          rect.SDL_UnionRect, None, None)
        self.assertRaises((AttributeError, TypeError),
                          rect.SDL_UnionRect, "Test", r2)
        self.assertRaises((AttributeError, TypeError),
                          rect.SDL_UnionRect, r1, None)
        self.assertRaises((AttributeError, TypeError),
                          rect.SDL_UnionRect, r1, "Test")

    def test_SDL_IntersectRectAndLine(self):
        r = rect.SDL_Rect()
        x1, y1, x2, y2 = c_int(-5), c_int(-5), c_int(5), c_int(5)
        ret = rect.SDL_IntersectRectAndLine(r, byref(x1), byref(y1),
                                            byref(x2), byref(y2))
        self.assertFalse(ret)

        r = rect.SDL_Rect(0, 0, 2, 2)
        x1, y1, x2, y2 = c_int(-1), c_int(-1), c_int(3), c_int(3)
        ret = rect.SDL_IntersectRectAndLine(r, byref(x1), byref(y1),
                                            byref(x2), byref(y2))
        self.assertTrue(ret)
        self.assertEqual((x1.value, y1.value, x2.value, y2.value),
                         (0, 0, 1, 1))

        r = rect.SDL_Rect(-4, -4, 14, 14)
        x1, y1, x2, y2 = c_int(8), c_int(22), c_int(8), c_int(33)
        ret = rect.SDL_IntersectRectAndLine(r, byref(x1), byref(y1),
                                            byref(x2), byref(y2))
        self.assertFalse(ret)
        # TODO

    def test_SDL_EnclosePoints(self):
        pt1 = rect.SDL_Point(0, 0)
        pt2 = rect.SDL_Point(5, 7)
        clip = rect.SDL_Rect(0, 0, 10, 10)
        res = rect.SDL_Rect()
        ret = rect.SDL_EnclosePoints(to_ctypes([pt1, pt2], rect.SDL_Point), 2,
                                     byref(clip), byref(res))
        self.assertTrue(ret)
        self.assertEqual(res, rect.SDL_Rect(0, 0, 6, 8))

        clip = rect.SDL_Rect(-10, -10, 3, 3)
        ret = rect.SDL_EnclosePoints(to_ctypes([pt1, pt2], rect.SDL_Point), 2,
                                     byref(clip), byref(res))
        self.assertFalse(ret)
        self.assertNotEqual(res, rect.SDL_Rect(0, 0, 0, 0))

        ret = rect.SDL_EnclosePoints(to_ctypes([pt1, pt2], rect.SDL_Point), 2,
                                     None, byref(res))
        self.assertTrue(ret)
        self.assertEqual(res, rect.SDL_Rect(0, 0, 6, 8))

        ret = rect.SDL_EnclosePoints(None, 0, None, byref(res))
        self.assertFalse(ret)
        self.assertNotEqual(res, rect.SDL_Rect())

        self.assertRaises(TypeError, rect.SDL_EnclosePoints, None, None)
        self.assertRaises(TypeError, rect.SDL_EnclosePoints, "Test", None)
        self.assertRaises(TypeError, rect.SDL_EnclosePoints, (1, 2, 3), None)
        self.assertRaises(TypeError, rect.SDL_EnclosePoints, (None,), None)

    def test_SDL_HasIntersection(self):
        r1 = rect.SDL_Rect()
        r2 = rect.SDL_Rect()
        self.assertFalse(rect.SDL_HasIntersection(r1, r2))

        r1 = rect.SDL_Rect(0, 0, -200, 200)
        r2 = rect.SDL_Rect(0, 0, -100, 200)
        self.assertFalse(rect.SDL_HasIntersection(r1, r2))

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, 5, 10, 2)
        self.assertTrue(rect.SDL_HasIntersection(r1, r2))

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 10, 2)
        self.assertFalse(rect.SDL_HasIntersection(r1, r2))

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 2, 10)
        self.assertFalse(rect.SDL_HasIntersection(r1, r2))

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 5, 5)
        self.assertFalse(rect.SDL_HasIntersection(r1, r2))

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 6, 6)
        self.assertTrue(rect.SDL_HasIntersection(r1, r2))

    def test_SDL_IntersectRect(self):
        r1 = rect.SDL_Rect()
        r2 = rect.SDL_Rect()
        res = rect.SDL_Rect()
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        self.assertFalse(ret)

        r1 = rect.SDL_Rect(0, 0, -200, 200)
        r2 = rect.SDL_Rect(0, 0, -100, 200)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        self.assertFalse(ret)

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, 5, 10, 2)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        self.assertTrue(ret)
        self.assertEqual(res, rect.SDL_Rect(0, 5, 5, 2))

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 10, 2)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        self.assertFalse(ret)

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 2, 10)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        self.assertFalse(ret)

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 5, 5)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        self.assertFalse(ret)

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 6, 6)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        self.assertTrue(ret)
        self.assertEqual(res, rect.SDL_Rect(0, 0, 1, 1))

    def test_SDL_PointInRect(self):
        r1 = rect.SDL_Rect(0, 0, 10, 10)
        p = rect.SDL_Point(0, 0)
        self.assertTrue(rect.SDL_PointInRect(p, r1))
        p = rect.SDL_Point(10, 10)
        self.assertFalse(rect.SDL_PointInRect(p, r1))
        p = rect.SDL_Point(10, 3)
        self.assertFalse(rect.SDL_PointInRect(p, r1))
        p = rect.SDL_Point(3, 10)
        self.assertFalse(rect.SDL_PointInRect(p, r1))
        p = rect.SDL_Point(4, 2)
        self.assertTrue(rect.SDL_PointInRect(p, r1))

if __name__ == '__main__':
    sys.exit(unittest.main())
