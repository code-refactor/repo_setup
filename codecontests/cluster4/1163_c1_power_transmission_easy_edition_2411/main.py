#!/usr/bin/env python3

from library import Point, get_slope, normalize_rational
from collections import defaultdict
import math

n = int(input())
points = [tuple(map(int, input().split())) for _ in range(n)]
result = 0

# Store lines as (slope, intercept) where slope is in normalized form
slopes = defaultdict(set)
for i in range(n - 1):
    for j in range(i + 1, n):
        x1, y1, x2, y2 = points[i][0], points[i][1], points[j][0], points[j][1]
        a, b = y1 - y2, x1 - x2  # a * x - b * y = c
        
        # Normalize coefficients
        d = abs(math.gcd(a, b))
        a, b = a // d, b // d
        
        # Ensure standard form for slope
        if a < 0 or (a == 0 and b < 0):
            a, b = -a, -b
        
        # Calculate c = a * x - b * y
        c = a * x1 - b * y1
        
        # Store in slopes dictionary
        slope = (a, b)
        slopes[slope].add(c)

# Count intersections
slopeGroups = [(ab[0], ab[1], len(cs)) for ab, cs in slopes.items()]
m = len(slopeGroups)

for i in range(m - 1):
    intersects = 0
    for j in range(i + 1, m):
        intersects += slopeGroups[j][2]
    result += slopeGroups[i][2] * intersects

print(str(result))