#!/usr/bin/env python3

from library import Point
from collections import Counter

# Read the 8 points
points = []
for _ in range(8):
    x, y = map(int, input().split())
    points.append(Point(x, y))

# Sort the points to make analysis easier
points.sort(key=lambda p: (p.x, p.y))

# Check if the points form a respectable eight point set
# Requirements:
# 1. There must be exactly 3 distinct x-coordinates
# 2. There must be exactly 3 distinct y-coordinates
# 3. The points must be all intersections of these coordinates, except for the center point (x2, y2)

# Count occurrences of x and y coordinates
x_counts = Counter(p.x for p in points)
y_counts = Counter(p.y for p in points)

# Check if there are exactly 3 distinct x and y coordinates
if len(x_counts) != 3 or len(y_counts) != 3:
    print("ugly")
    exit()

# Sort the distinct x and y coordinates
x_coords = sorted(x_counts.keys())
y_coords = sorted(y_counts.keys())

# Create the expected set of 8 points (all 9 intersections except the center)
expected_points = set()
for x in x_coords:
    for y in y_coords:
        # Skip the center point (x2, y2)
        if x == x_coords[1] and y == y_coords[1]:
            continue
        expected_points.add((x, y))

# Check if the given points match the expected set
actual_points = set((p.x, p.y) for p in points)

if actual_points == expected_points:
    print("respectable")
else:
    print("ugly")