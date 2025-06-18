#!/usr/bin/env python3

from library import Point, Line
from collections import defaultdict
import math

n = int(input())
points = [Point(*(map(int, input().split()))) for _ in range(n)]

# Group lines by their slopes and intercepts
directions = defaultdict(set)
for i in range(n):
    for j in range(i+1, n):
        p1, p2 = points[i], points[j]
        
        # Create a line from two points
        line = Line(p1, p2)
        
        # Use canonical form (Ax + By + C = 0) to represent the line
        a, b, c = line.get_canonical_form()
        
        # Normalize coefficients
        if a < 0 or (a == 0 and b < 0):
            a, b, c = -a, -b, -c
            
        # Use slope as key and intercept as value in the set
        if abs(a) < 1e-9:  # Horizontal line
            slope_key = (0, 1)
            intercept = -c/b
        elif abs(b) < 1e-9:  # Vertical line
            slope_key = (1, 0)
            intercept = -c/a
        else:
            # Normalize to make a = 1
            b /= a
            c /= a
            slope_key = (1, b)
            intercept = -c
            
        directions[slope_key].add(intercept)

# Calculate total number of lines
total_lines = sum(len(value) for value in directions.values())

# Count intersections
result = 0
for value in directions.values():
    current = len(value)
    result += (total_lines - current) * current

print(int(result / 2))