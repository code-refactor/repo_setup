#!/usr/bin/env python3

from library import Point, get_slope, setup_io
from collections import defaultdict
from math import gcd

input = setup_io()

n = int(input())
points = []
for _ in range(n):
    x, y = map(int, input().split())
    points.append(Point(x, y))

total_triangles = 0

for i, point in enumerate(points):
    slope_counts = defaultdict(int)
    
    for other_point in points:
        if point == other_point:
            continue
            
        # Calculate the normalized slope vector from current point to other point
        dx = other_point.x - point.x
        dy = other_point.y - point.y
        
        # Normalize direction
        if dx < 0 or (dx == 0 and dy < 0):
            dx, dy = -dx, -dy
        
        # Reduce by gcd
        g = abs(gcd(dx, dy))
        dx //= g
        dy //= g
        
        slope_counts[(dx, dy)] += 1
    
    # Count triangles formed with current point
    point_triangles = 0
    for count in slope_counts.values():
        # For each slope direction, count triangles with points in other directions
        point_triangles += count * (n - 1 - count)
    
    total_triangles += point_triangles // 2

# Each triangle is counted 3 times (once for each vertex)
print(total_triangles // 3)