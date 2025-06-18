#!/usr/bin/env python3

from library import Point

def a(x1, y1, x2, y2, x3, y3, x4, y4):
    """Check if two line segments intersect"""
    if x1 == x2:
        if x3 == x4:
            return False
        else:
            k2 = (y3 - y4) / (x3 - x4)
            b2 = y3 - k2 * x3
            return min(y3, y4) <= k2 * x1 + b2 <= max(y3, y4) and min(y1, y2) <= k2 * x1 + b2 <= max(y1, y2) and min(x3, x4) <= x1 <= max(x3, x4) and min(x1, x2) <= x1 <= max(x1, x2)
    else:
        if x3 == x4:
            k1 = (y1 - y2) / (x1 - x2)
            b1 = y1 - k1 * x1
            return min(y3, y4) <= k1 * x3 + b1 <= max(y3, y4) and min(y1, y2) <= k1 * x3 + b1 <= max(y1, y2) and min(x3, x4) <= x3 <= max(x3, x4) and min(x1, x2) <= x3 <= max(x1, x2)
        else:
            k1 = (y1 - y2) / (x1 - x2)
            b1 = y1 - k1 * x1
            k2 = (y3 - y4) / (x3 - x4)
            b2 = y3 - k2 * x3
            if k1 == k2:
                return b1 == b2 and min(x1, x2) <= min(x3, x4) <= max(x1, x2) and min(y1, y2) <= min(y3, y4) <= max(y1, y2)
            x = (b2 - b1) / (k1 - k2)
            y = k1 * x + b1
            return min(y3, y4) <= y <= max(y3, y4) and min(y1, y2) <= y <= max(y1, y2) and min(x3, x4) <= x <= max(x3, x4) and min(x1, x2) <= x <= max(x1, x2)

def b(xm1, xm2, ym1, ym2, x, y):
    """Reflect a point across a line"""
    if ym1 == ym2:
        xi = x
        yi = 2 * ym1 - y
    elif xm1 == xm2:
        yi = y
        xi = 2 * xm1 - x
    else:
        k1 = -(xm1 - xm2) / (ym1 - ym2)
        b1 = y - k1 * x
        k2 = (ym1 - ym2) / (xm1 - xm2)
        b2 = ym1 - k2 * xm1
        x1 = (b2 - b1) / (k1 - k2)
        xi = 2 * x1 - x
        yi = k1 * xi + b1
    return [xi, yi]

# Read input coordinates
xv, yv = map(int, input().split())
xp, yp = map(int, input().split())
xw1, yw1, xw2, yw2 = map(int, input().split())
xm1, ym1, xm2, ym2 = map(int, input().split())

# Calculate reflections
xw3, yw3 = b(xm1, xm2, ym1, ym2, xw1, yw1)
xw4, yw4 = b(xm1, xm2, ym1, ym2, xw2, yw2)

# Check if direct path is blocked
if a(xv, yv, xp, yp, xw1, yw1, xw2, yw2) or a(xv, yv, xp, yp, xm1, ym1, xm2, ym2):
    # Direct path is blocked, check if reflection works
    xip, yip = b(xm1, xm2, ym1, ym2, xp, yp)
    
    # Reflection must hit mirror, but not walls
    if [xip, yip] != [xv, yv] and a(xv, yv, xip, yip, xm1, ym1, xm2, ym2) and not(a(xv, yv, xip, yip, xw1, yw1, xw2, yw2)) and not(a(xv, yv, xip, yip, xw3, yw3, xw4, yw4)):
        print('YES')
    else:
        print('NO')
else:
    # Direct path is not blocked
    print('YES')