#!/usr/bin/env python3

from library import Point, cross_product

# Calculate vector between two points
def vector(p1, p2):
    return (p2[0] - p1[0], p2[1] - p1[1])

# Read input
n = int(input())
points = []
for _ in range(n + 1):
    x, y = map(int, input().split())
    points.append((x, y))

# Count dangerous turns
# A turn is dangerous if ignoring it would lead to the water
# This happens when the cross product of consecutive vectors is negative
# (representing a right turn)
dangerous_turns = 0
for i in range(2, n):
    v1 = vector(points[i], points[i-1])
    v2 = vector(points[i-1], points[i-2])
    
    # Calculate the cross product
    # v1 × v2 = v1.x * v2.y - v1.y * v2.x
    cross = v1[0] * v2[1] - v1[1] * v2[0]
    
    # If cross product is negative, it's a right turn (dangerous)
    if cross < 0:
        dangerous_turns += 1

print(dangerous_turns)