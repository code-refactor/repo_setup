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
    
    # Check if start and end points are on different sides of the line (ax + by + c = 0)
    if b != 0:
        # Line is not vertical, so we can express it as y = -ax/b - c/b
        # For a non-vertical line, we can test if points are on different sides
        # by checking the sign of the expression: x*(y1-y0) - (y-y0)
        # where (0, y0) is a point on the line
        
        y00 = -c / b  # y-intercept where x = 0
        y01 = -(a + c) / b  # y value when x = 1
        
        # Calculate sign of cross product to determine side of line
        s1 = x1 * (y01 - y00) - (y1 - y00)
        s2 = x2 * (y01 - y00) - (y2 - y00)
        
        if (s1 < 0 < s2) or (s1 > 0 > s2):
            crossings += 1
    else:
        # Line is vertical (x = -c/a)
        x = -c / a
        if (x1 < x < x2) or (x1 > x > x2):
            crossings += 1

print(crossings)