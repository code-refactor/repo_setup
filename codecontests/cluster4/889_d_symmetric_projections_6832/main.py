#!/usr/bin/env python3

from fractions import Fraction
from library import Point

def abs_sgn(x):
    """Return the absolute value and sign of x"""
    if x == 0:
        return 0, 0
    if x < 0:
        return -x, -1
    return x, 1

def solve(tuple_points):
    """Solve the symmetric projections problem using our original approach to avoid precision issues"""
    # Just reimplement the original working algorithm
    points = set()
    center = Point(0, 0)
    for x, y in tuple_points:
        cur = Point(x * 2 * n, y * 2 * n)
        center += cur
        points.add(cur)

    center.x //= n
    center.y //= n
    dcenter = Point(center.x * 2, center.y * 2)

    # Find points without symmetry
    sym_points_set = set()
    for p in points:
        sym_points_set.add(Point(dcenter.x - p.x, dcenter.y - p.y))
    nosym = list(points - sym_points_set)

    # If all points have symmetry, return -1
    if len(nosym) == 0:
        return -1

    p0 = nosym[0]
    good_lines = set()
    
    for p in nosym:
        # Calculate midpoint
        m = Point((p.x + p0.x) // 2, (p.y + p0.y) // 2)
        
        # Define line through midpoint and center
        a = m.y - center.y
        b = center.x - m.x
        c = m.x * center.y - m.y * center.x
        
        # Calculate distances
        distances = [a * p.x + b * p.y + c for p in nosym]
        
        # Check symmetry
        ok = True
        distance_counts = {}
        for d in distances:
            d_abs, sgn = abs_sgn(d)
            if d_abs not in distance_counts:
                distance_counts[d_abs] = sgn
            else:
                distance_counts[d_abs] += sgn
                
        for k in distance_counts:
            if distance_counts[k] != 0:
                ok = False
                break
                
        # If symmetry is found, add the line direction
        if ok:
            if a == 0:
                good_lines.add((0, 1))  # Horizontal line
            else:
                # Represent slope as direction
                if b == 0:
                    direction = (1, 0)  # Vertical line
                else:
                    try:
                        direction = (1, Fraction(b, a))
                    except ZeroDivisionError:
                        direction = (1, 0)  # Vertical line
                good_lines.add(direction)
    
    return len(good_lines)

if __name__ == "__main__":
    n = int(input())
    pts = []
    for _ in range(n):
        x, y = map(int, input().split())
        pts.append((x, y))
    print(solve(pts))