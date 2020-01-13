import sys
import copy
import pytest
from ctypes import byref, c_int
from sdl2 import rect

to_ctypes = lambda seq, dtype: (dtype * len(seq))(*seq)


class TestSDLRect(object):
    __tags__ = ["sdl"]

    def test_SDL_Point(self):
        pt = rect.SDL_Point()
        assert (pt.x, pt.y) == (0, 0)
        for x in range(-100, 100):
            for y in range(-100, 100):
                pt = rect.SDL_Point(x, y)
                assert (pt.x, pt.y) == (x, y)

    def test_SDL_Point_x(self):
        pt = rect.SDL_Point()

        def setx(point, val):
            point.x = val

        for x in range(-1000, 1000):
            pt.x = x
            assert (pt.x, pt.y) == (x, 0)

        with pytest.raises(TypeError):
            setx(pt, 10.4)
        with pytest.raises(TypeError):
            setx(pt, "Test")
        with pytest.raises(TypeError):
            setx(pt, None)

    def test_SDL_Point_y(self):
        pt = rect.SDL_Point()

        def sety(point, val):
            point.y = val

        for x in range(-1000, 1000):
            pt.y = x
            assert (pt.x, pt.y) == (0, x)

        with pytest.raises(TypeError):
            sety(pt, 10.4)
        with pytest.raises(TypeError):
            sety(pt, "Test")
        with pytest.raises(TypeError):
            sety(pt, None)

    def test_SDL_Point__repr__(self):
        pt = rect.SDL_Point()
        pt2 = eval("rect.%s" % repr(pt))
        assert pt == pt2
        assert (pt.x, pt.y) == (pt2.x, pt2.y)

        pt = rect.SDL_Point(10, 12)
        pt2 = eval("rect.%s" % repr(pt))
        assert pt == pt2
        assert (pt.x, pt.y) == (pt2.x, pt2.y)

    def test_SDL_Point__copy__(self):
        pt = rect.SDL_Point()
        pt2 = copy.copy(pt)
        assert pt == pt2
        assert (pt.x, pt.y) == (pt2.x, pt2.y)

        pt2.x = 7
        pt2.y = 9

        pt3 = copy.copy(pt2)
        assert pt != pt2
        assert pt3 == pt2

    def test_SDL_Point__eq__(self):
        assert rect.SDL_Point() == rect.SDL_Point()
        assert rect.SDL_Point(0, 0) == rect.SDL_Point(0, 0)
        assert rect.SDL_Point(10, 0) == rect.SDL_Point(10, 0)
        assert rect.SDL_Point(0, 10) == rect.SDL_Point(0, 10)
        assert rect.SDL_Point(12, 10) == rect.SDL_Point(12, 10)

        assert not (rect.SDL_Point(0, 0) == rect.SDL_Point(0, 1))
        assert not (rect.SDL_Point(0, 0) == rect.SDL_Point(1, 0))
        assert not (rect.SDL_Point(0, 0) == rect.SDL_Point(1, 1))

        assert not (rect.SDL_Point(10, 10) == rect.SDL_Point(10, 0))
        assert not (rect.SDL_Point(7, 10) == rect.SDL_Point(0, 10))
        assert not (rect.SDL_Point(12, 10) == rect.SDL_Point(12, 11))

    def test_SDL_Point__ne__(self):
        assert not (rect.SDL_Point() != rect.SDL_Point())
        assert not (rect.SDL_Point(0, 0) != rect.SDL_Point(0, 0))
        assert not (rect.SDL_Point(10, 0) != rect.SDL_Point(10, 0))
        assert not (rect.SDL_Point(0, 10) != rect.SDL_Point(0, 10))
        assert not (rect.SDL_Point(12, 10) != rect.SDL_Point(12, 10))

        assert rect.SDL_Point(0, 0) != rect.SDL_Point(0, 1)
        assert rect.SDL_Point(0, 0) != rect.SDL_Point(1, 0)
        assert rect.SDL_Point(0, 0) != rect.SDL_Point(1, 1)

        assert rect.SDL_Point(10, 10) != rect.SDL_Point(10, 0)
        assert rect.SDL_Point(7, 10) != rect.SDL_Point(0, 10)
        assert rect.SDL_Point(12, 10) != rect.SDL_Point(12, 11)

    def test_SDL_Rect(self):
        rt = rect.SDL_Rect()
        assert (rt.x, rt.y, rt.w, rt.h) == (0, 0, 0, 0)
        for x in range(-10, 10):
            for y in range(-10, 10):
                for w in range(-10, 10):
                    for h in range(-10, 10):
                        rt = rect.SDL_Rect(x, y, w, h)
                        assert (rt.x, rt.y, rt.w, rt.h) == (x, y, w, h)

    def test_SDL_Rect__repr__(self):
        rt = rect.SDL_Rect(1, 2, 3, 4)
        rt2 = eval("rect.%s" % repr(rt))
        assert (rt.x, rt.y, rt.w, rt.h) == (rt2.x, rt2.y, rt2.w, rt2.h)
        assert rt == rt2

    def test_SDL_Rect__copy__(self):
        rt = rect.SDL_Rect()
        rt2 = copy.copy(rt)
        assert rt == rt2
        assert (rt.x, rt.y, rt.w, rt.h) == (rt2.x, rt2.y, rt2.w, rt2.h)

        rt2.x = 5
        rt2.y = 33
        rt2.w = 17
        rt2.w = 212

        rt3 = copy.copy(rt2)
        assert rt != rt2
        assert rt3 == rt2

    def test_SDL_Rect__eq__(self):
        sdlr = rect.SDL_Rect

        assert sdlr() == sdlr()
        assert sdlr(0, 0, 0, 0) == sdlr(0, 0, 0, 0)
        assert sdlr(1, 2, 3, 4) == sdlr(1, 2, 3, 4)
        assert sdlr(-1, -2, -3, -4) == sdlr(-1, -2, -3, -4)

        assert sdlr(10, 0, 0, 0) == sdlr(10, 0, 0, 0)
        assert sdlr(0, 10, 0, 0) == sdlr(0, 10, 0, 0)
        assert sdlr(0, 0, 10, 0) == sdlr(0, 0, 10, 0)
        assert sdlr(0, 0, 0, 10) == sdlr(0, 0, 0, 10)

        assert sdlr(10, 10, 0, 0) == sdlr(10, 10, 0, 0)
        assert sdlr(0, 10, 10, 0) == sdlr(0, 10, 10, 0)
        assert sdlr(0, 0, 10, 10) == sdlr(0, 0, 10, 10)
        assert sdlr(10, 0, 0, 10) == sdlr(10, 0, 0, 10)

        assert sdlr(10, 10, 10, 0) == sdlr(10, 10, 10, 0)
        assert sdlr(0, 10, 10, 10) == sdlr(0, 10, 10, 10)

        assert not (sdlr() == sdlr(0, 0, 0, 1))
        assert not (sdlr(10, 0, 0, 0) == sdlr(0, 0, 0, 0))
        assert not (sdlr(10, 10, 0, 0) == sdlr(0, 10, 0, 0))
        assert not (sdlr(10, 0, 10, 0) == sdlr(0, 0, 10, 0))
        assert not (sdlr(10, 0, 0, 10) == sdlr(0, 0, 0, 10))
        assert not (sdlr(1, 2, 3, 4) == sdlr(-1, -2, -3, -4))

    def test_SDL_Rect__ne__(self):
        sdlr = rect.SDL_Rect

        assert sdlr() != sdlr(0, 0, 0, 1)
        assert sdlr(10, 0, 0, 0) != sdlr(0, 0, 0, 0)
        assert sdlr(10, 10, 0, 0) != sdlr(0, 10, 0, 0)
        assert sdlr(10, 0, 10, 0) != sdlr(0, 0, 10, 0)
        assert sdlr(10, 0, 0, 10) != sdlr(0, 0, 0, 10)
        assert sdlr(1, 2, 3, 4) != sdlr(-1, -2, -3, -4)

        assert not (sdlr() != sdlr())
        assert not (sdlr(0, 0, 0, 0) != sdlr(0, 0, 0, 0))
        assert not (sdlr(1, 2, 3, 4) != sdlr(1, 2, 3, 4))
        assert not (sdlr(-1, -2, -3, -4) != sdlr(-1, -2, -3, -4))

        assert not (sdlr(10, 0, 0, 0) != sdlr(10, 0, 0, 0))
        assert not (sdlr(0, 10, 0, 0) != sdlr(0, 10, 0, 0))
        assert not (sdlr(0, 0, 10, 0) != sdlr(0, 0, 10, 0))
        assert not (sdlr(0, 0, 0, 10) != sdlr(0, 0, 0, 10))

        assert not (sdlr(10, 10, 0, 0) != sdlr(10, 10, 0, 0))
        assert not (sdlr(0, 10, 10, 0) != sdlr(0, 10, 10, 0))
        assert not (sdlr(0, 0, 10, 10) != sdlr(0, 0, 10, 10))
        assert not (sdlr(10, 0, 0, 10) != sdlr(10, 0, 0, 10))

        assert not (sdlr(10, 10, 10, 0) != sdlr(10, 10, 10, 0))
        assert not (sdlr(0, 10, 10, 10) != sdlr(0, 10, 10, 10))

    def test_SDL_Rect_x(self):
        rt = rect.SDL_Rect()

        def setx(r, val):
            r.x = val

        for x in range(-1000, 1000):
            rt.x = x
            assert (rt.x, rt.y, rt.w, rt.h) == (x, 0, 0, 0)

        with pytest.raises(TypeError):
            setx(rt, 10.4)
        with pytest.raises(TypeError):
            setx(rt, "Test")
        with pytest.raises(TypeError):
            setx(rt, None)

    def test_SDL_Rect_y(self):
        rt = rect.SDL_Rect()

        def sety(r, val):
            r.y = val

        for x in range(-1000, 1000):
            rt.y = x
            assert (rt.x, rt.y, rt.w, rt.h) == (0, x, 0, 0)

        with pytest.raises(TypeError):
            sety(rt, 10.4)
        with pytest.raises(TypeError):
            sety(rt, "Test")
        with pytest.raises(TypeError):
            sety(rt, None)

    def test_SDL_Rect_w(self):
        rt = rect.SDL_Rect()

        def setw(r, val):
            r.w = val

        for x in range(-1000, 1000):
            rt.w = x
            assert (rt.x, rt.y, rt.w, rt.h) == (0, 0, x, 0)

        with pytest.raises(TypeError):
            setw(rt, 10.4)
        with pytest.raises(TypeError):
            setw(rt, "Test")
        with pytest.raises(TypeError):
            setw(rt, None)

    def test_SDL_Rect_h(self):
        rt = rect.SDL_Rect()

        def seth(r, val):
            r.h = val

        for x in range(-1000, 1000):
            rt.h = x
            assert (rt.x, rt.y, rt.w, rt.h) == (0, 0, 0, x)

        with pytest.raises(TypeError):
            seth(rt, 10.4)
        with pytest.raises(TypeError):
            seth(rt, "Test")
        with pytest.raises(TypeError):
            seth(rt, None)

    def test_SDL_RectEmpty(self):
        for w in range(-100, 100):
            for h in range(-100, 100):
                r = rect.SDL_Rect(0, 0, w, h)
                if w > 0 and h > 0:
                    assert not rect.SDL_RectEmpty(r)
                else:
                    assert rect.SDL_RectEmpty(r)
        with pytest.raises(AttributeError):
            rect.SDL_RectEmpty("Test")

    def test_SDL_RectEquals(self):
        r1 = rect.SDL_Rect(0, 0, 0, 0)
        r2 = rect.SDL_Rect(0, 0, 0, 0)
        assert rect.SDL_RectEquals(r1, r2)
        assert r1 == r2
        r2 = rect.SDL_Rect(-1, 2, 0, 0)
        assert not rect.SDL_RectEquals(r1, r2)
        assert r1 != r2
        r2 = rect.SDL_Rect(0, 0, 1, 2)
        assert not rect.SDL_RectEquals(r1, r2)
        assert r1 != r2
        with pytest.raises(AttributeError):
            rect.SDL_RectEquals("Test", r2)
        with pytest.raises(AttributeError):
            rect.SDL_RectEquals(r1, None)
        with pytest.raises(AttributeError):
            rect.SDL_RectEquals(r1, "Test")

    def test_SDL_UnionRect(self):
        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(20, 20, 10, 10)
        r3 = rect.SDL_Rect()
        rect.SDL_UnionRect(r1, r2, byref(r3))
        assert (r3.x, r3.y, r3.w, r3.h) == (0, 0, 30, 30)

        r1 = rect.SDL_Rect(0, 0, 0, 0)
        r2 = rect.SDL_Rect(20, 20, 10, 10)
        rect.SDL_UnionRect(r1, r2, byref(r3))
        assert (r3.x, r3.y, r3.w, r3.h) == (20, 20, 10, 10)

        r1 = rect.SDL_Rect(-200, -4, 450, 33)
        r2 = rect.SDL_Rect(20, 20, 10, 10)
        rect.SDL_UnionRect(r1, r2, byref(r3))
        assert (r3.x, r3.y, r3.w, r3.h) == (-200, -4, 450, 34)

        r1 = rect.SDL_Rect(0, 0, 15, 16)
        r2 = rect.SDL_Rect(20, 20, 0, 0)
        rect.SDL_UnionRect(r1, r2, byref(r3))
        assert (r3.x, r3.y, r3.w, r3.h) == (0, 0, 15, 16)

        with pytest.raises((AttributeError, TypeError)):
            rect.SDL_UnionRect(None, None)
        with pytest.raises((AttributeError, TypeError)):
            rect.SDL_UnionRect("Test", r2)
        with pytest.raises((AttributeError, TypeError)):
            rect.SDL_UnionRect(r1, None)
        with pytest.raises((AttributeError, TypeError)):
            rect.SDL_UnionRect(r1, "Test")

    def test_SDL_IntersectRectAndLine(self):
        r = rect.SDL_Rect()
        x1, y1, x2, y2 = c_int(-5), c_int(-5), c_int(5), c_int(5)
        ret = rect.SDL_IntersectRectAndLine(r, byref(x1), byref(y1),
                                            byref(x2), byref(y2))
        assert not ret

        r = rect.SDL_Rect(0, 0, 2, 2)
        x1, y1, x2, y2 = c_int(-1), c_int(-1), c_int(3), c_int(3)
        ret = rect.SDL_IntersectRectAndLine(r, byref(x1), byref(y1),
                                            byref(x2), byref(y2))
        assert ret
        assert (x1.value, y1.value, x2.value, y2.value) == (0, 0, 1, 1)

        r = rect.SDL_Rect(-4, -4, 14, 14)
        x1, y1, x2, y2 = c_int(8), c_int(22), c_int(8), c_int(33)
        ret = rect.SDL_IntersectRectAndLine(r, byref(x1), byref(y1),
                                            byref(x2), byref(y2))
        assert not ret
        # TODO

    def test_SDL_EnclosePoints(self):
        pt1 = rect.SDL_Point(0, 0)
        pt2 = rect.SDL_Point(5, 7)
        clip = rect.SDL_Rect(0, 0, 10, 10)
        res = rect.SDL_Rect()
        ret = rect.SDL_EnclosePoints(to_ctypes([pt1, pt2], rect.SDL_Point), 2,
                                     byref(clip), byref(res))
        assert ret
        assert res == rect.SDL_Rect(0, 0, 6, 8)

        clip = rect.SDL_Rect(-10, -10, 3, 3)
        ret = rect.SDL_EnclosePoints(to_ctypes([pt1, pt2], rect.SDL_Point), 2,
                                     byref(clip), byref(res))
        assert not ret
        assert res != rect.SDL_Rect(0, 0, 0, 0)

        ret = rect.SDL_EnclosePoints(to_ctypes([pt1, pt2], rect.SDL_Point), 2,
                                     None, byref(res))
        assert ret
        assert res == rect.SDL_Rect(0, 0, 6, 8)

        ret = rect.SDL_EnclosePoints(None, 0, None, byref(res))
        assert not ret
        assert res != rect.SDL_Rect()

        with pytest.raises(TypeError):
            rect.SDL_EnclosePoints(None, None)
        with pytest.raises(TypeError):
            rect.SDL_EnclosePoints("Test", None)
        with pytest.raises(TypeError):
            rect.SDL_EnclosePoints((1, 2, 3), None)
        with pytest.raises(TypeError):
            rect.SDL_EnclosePoints((None,), None)

    def test_SDL_HasIntersection(self):
        r1 = rect.SDL_Rect()
        r2 = rect.SDL_Rect()
        assert not rect.SDL_HasIntersection(r1, r2)

        r1 = rect.SDL_Rect(0, 0, -200, 200)
        r2 = rect.SDL_Rect(0, 0, -100, 200)
        assert not rect.SDL_HasIntersection(r1, r2)

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, 5, 10, 2)
        assert rect.SDL_HasIntersection(r1, r2)

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 10, 2)
        assert not rect.SDL_HasIntersection(r1, r2)

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 2, 10)
        assert not rect.SDL_HasIntersection(r1, r2)

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 5, 5)
        assert not rect.SDL_HasIntersection(r1, r2)

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 6, 6)
        assert rect.SDL_HasIntersection(r1, r2)

    def test_SDL_IntersectRect(self):
        r1 = rect.SDL_Rect()
        r2 = rect.SDL_Rect()
        res = rect.SDL_Rect()
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        assert not ret

        r1 = rect.SDL_Rect(0, 0, -200, 200)
        r2 = rect.SDL_Rect(0, 0, -100, 200)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        assert not ret

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, 5, 10, 2)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        assert ret
        assert res == rect.SDL_Rect(0, 5, 5, 2)

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 10, 2)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        assert not ret

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 2, 10)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        assert not ret

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 5, 5)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        assert not ret

        r1 = rect.SDL_Rect(0, 0, 10, 10)
        r2 = rect.SDL_Rect(-5, -5, 6, 6)
        ret = rect.SDL_IntersectRect(r1, r2, byref(res))
        assert ret
        assert res == rect.SDL_Rect(0, 0, 1, 1)

    def test_SDL_PointInRect(self):
        r1 = rect.SDL_Rect(0, 0, 10, 10)
        p = rect.SDL_Point(0, 0)
        assert rect.SDL_PointInRect(p, r1)
        p = rect.SDL_Point(10, 10)
        assert not rect.SDL_PointInRect(p, r1)
        p = rect.SDL_Point(10, 3)
        assert not rect.SDL_PointInRect(p, r1)
        p = rect.SDL_Point(3, 10)
        assert not rect.SDL_PointInRect(p, r1)
        p = rect.SDL_Point(4, 2)
        assert rect.SDL_PointInRect(p, r1)
