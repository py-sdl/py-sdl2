.. currentmodule:: sdl2.ext

Common algorithms
=================

.. function:: cohensutherland(left : int, top : int, right : int, \
   bottom : int, x1 : int, y1 : int, x2 : int, y2 : int) -> int, int, int, int

   This implements the Cohen-Sutherland line clipping
   algorithm. *left*, *top*, *right* and *bottom* denote the
   clipping area, into which the line defined by *x1*, *y1* (start
   point) and *x2*, *y2* (end point) will be clipped.

   If the line does not intersect with the rectangular clipping area,
   four ``None`` values will be returned as tuple. Otherwise a tuple of
   the clipped line points will be returned in the form ``(cx1, cy1,
   cx2, cy2)``.

.. function:: liangbarsky(left : int, top : int, right : int, \
   bottom : int, x1 : int, y1 : int, x2 : int, y2 : int) -> int, int, int, int

   This implements the Liang-Barsky line clipping algorithm. *left*,
   *top*, *right* and *bottom* denote the clipping area, into
   which the line defined by *x1*, *y1* (start point) and *x2*,
   *y2* (end point) will be clipped.

   If the line does not intersect with the rectangular clipping area,
   four ``None`` values will be returned as tuple. Otherwise a tuple of
   the clipped line points will be returned in the form ``(cx1, cy1,
   cx2, cy2)``.

.. function:: clipline(left : int, top : int, right : int, \
   bottom : int, x1 : int, y1 : int, x2 : int, \
   y2 : int[,method=liangbarsky]) -> int, int, int, int

   Clips a line to a rectangular area.

.. function:: point_on_line(p1 : iterable, p2 : iterable, point : iterable) -> bool

   Checks, if *point*, a two-value tuple, is on the line segment defined by *p1*
   and *p2*.

