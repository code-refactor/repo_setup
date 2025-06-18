#!/usr/bin/env python3

from library import Point

# Read starting and ending points
x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
start = Point(x1, y1)
end = Point(x2, y2)

n = int(input())
crossings = 0

for _ in range(n):
    a, b, c = map(int, input().split())
    
    # Evaluating line equation Ax + By + C for a point
    # If the result is positive, the point is on one side of the line
    # If the result is negative, the point is on the other side
    
    # Check if start and end points are on different sides of the line
    start_side = a * start.x + b * start.y + c
    end_side = a * end.x + b * end.y + c
    
    # If the signs are different, the path crosses the line
    if (start_side > 0 and end_side < 0) or (start_side < 0 and end_side > 0):
        crossings += 1

print(crossings)