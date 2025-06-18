#!/usr/bin/env python3

from library import Point

# Read the three points
a = list(map(int, input().split()))
b = list(map(int, input().split()))
c = list(map(int, input().split()))

# Initialize counters for analyzing collinearity
x_collinear = 1  # Default: no points share the same x-coordinate
y_collinear = 1  # Default: no points share the same y-coordinate
intermediate_point = 0  # Counts if a point is between the other two points

# Check for points with the same x-coordinate
if a[0] == b[0] or a[0] == c[0] or b[0] == c[0]:
    x_collinear = 2  # At least two points have the same x
    
    # Check if all three points have the same x
    if a[0] == b[0] == c[0]:
        x_collinear = 3
    else:
        # Check if the third point is between the two collinear points (on y-axis)
        if a[0] == b[0]:
            if min(a[1], b[1]) < c[1] < max(a[1], b[1]):
                intermediate_point += 1
        elif a[0] == c[0]:
            if min(a[1], c[1]) < b[1] < max(a[1], c[1]):
                intermediate_point += 1
        elif b[0] == c[0]:
            if min(b[1], c[1]) < a[1] < max(b[1], c[1]):
                intermediate_point += 1

# Check for points with the same y-coordinate
if a[1] == b[1] or a[1] == c[1] or b[1] == c[1]:
    y_collinear = 2  # At least two points have the same y
    
    # Check if all three points have the same y
    if a[1] == b[1] == c[1]:
        y_collinear = 3
    else:
        # Check if the third point is between the two collinear points (on x-axis)
        if a[1] == b[1]:
            if min(a[0], b[0]) < c[0] < max(a[0], b[0]):
                intermediate_point += 1
        elif a[1] == c[1]:
            if min(a[0], c[0]) < b[0] < max(a[0], c[0]):
                intermediate_point += 1
        elif b[1] == c[1]:
            if min(b[0], c[0]) < a[0] < max(b[0], c[0]):
                intermediate_point += 1

# Determine the minimum number of segments needed
if x_collinear * y_collinear == 1:
    # No collinearity at all - need 3 segments
    print(3)
elif x_collinear * y_collinear == 3:
    # All points are on one line (either horizontally or vertically)
    print(1)
elif x_collinear * y_collinear == 4:
    # Both have value 2, meaning we have two collinear points on both axes
    print(2)
else:
    # Some collinearity exists, but not complete
    if intermediate_point == 1:
        # One point is between the other two, which forces us to use 3 segments
        print(3)
    else:
        # We can use 2 segments
        print(2)