"""Common algorithms."""

__all__ = ["liangbarsky", "cohensutherland", "clipline"]


def cohensutherland(left, top, right, bottom, x1, y1, x2, y2):
    """Clips a line to a rectangular area.

    This implements the Cohen-Sutherland line clipping algorithm.  left,
    top, right and bottom denote the clipping area, into which the line
    defined by x1, y1 (start point) and x2, y2 (end point) will be
    clipped.

    If the line does not intersect with the rectangular clipping area,
    four None values will be returned as tuple. Otherwise a tuple of the
    clipped line points will be returned in the form (cx1, cy1, cx2, cy2).
    """
    LEFT, RIGHT, LOWER, UPPER = 1, 2, 4, 8

    def _getclip(xa, ya):
        p = 0
        if xa < left:
            p = LEFT
        elif xa > right:
            p = RIGHT
        if ya < top:
            p |= LOWER
        elif ya > bottom:
            p |= UPPER
        return p

    k1 = _getclip(x1, y1)
    k2 = _getclip(x2, y2)
    while (k1 | k2) != 0:
        if (k1 & k2) != 0:
            return None, None, None, None
        opt = k1 or k2
        if opt & UPPER:
            x = x1 + (x2 - x1) * (1.0 * (bottom - y1)) / (y2 - y1)
            y = bottom
        elif opt & LOWER:
            x = x1 + (x2 - x1) * (1.0 * (top - y1)) / (y2 - y1)
            y = top
        elif opt & RIGHT:
            y = y1 + (y2 - y1) * (1.0 * (right - x1)) / (x2 - x1)
            x = right
        else:
            y = y1 + (y2 - y1) * (1.0 * (left - x1)) / (x2 - x1)
            x = right
        if opt == k1:
            x1, y1 = int(x), int(y)
            k1 = _getclip(x1, y1)
        else:
            x2, y2 = int(x), int(y)
            k2 = _getclip(x2, y2)
    return x1, y1, x2, y2


def liangbarsky(left, top, right, bottom, x1, y1, x2, y2):
    """Clips a line to a rectangular area.

    This implements the Liang-Barsky line clipping algorithm.  left,
    top, right and bottom denote the clipping area, into which the line
    defined by x1, y1 (start point) and x2, y2 (end point) will be
    clipped.

    If the line does not intersect with the rectangular clipping area,
    four None values will be returned as tuple. Otherwise a tuple of the
    clipped line points will be returned in the form (cx1, cy1, cx2, cy2).
    """
    dx = x2 - x1
    dy = y2 - y1
    dt0, dt1 = 0, 1

    checks = ((-dx, x1 - left),
              (dx, right - x1),
              (-dy, y1 - top),
              (dy, bottom - y1))

    for p, q in checks:
        if p == 0 and q < 0:
            return None, None, None, None
        dt = q / (p * 1.0)
        if p < 0:
            if dt > dt1:
                return None, None, None, None
            dt0 = max(dt0, dt)
        else:
            if dt < dt0:
                return None, None, None, None
            dt1 = min(dt1, dt)
    if dt0 > 0:
        x1 += dt0 * dx
        y1 += dt0 * dy
    if dt1 < 1:
        x2 = x1 + dt1 * dx
        y2 = y1 + dt1 * dy
    return x1, y1, x2, y2


clipline = lambda l, t, r, b, x1, y1, x2, y2, method = liangbarsky: \
    method(l, t, r, b, x1, y1, x2, y2)
