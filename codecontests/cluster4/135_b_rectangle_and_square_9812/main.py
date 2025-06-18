#!/usr/bin/env python3

from library import Point
from math import sqrt, asin, degrees

def is_square(p1, p2, p3, p4):
    """
    Check if 4 points form a square
    Steps:
    1. Sort the points to get a predictable ordering
    2. Verify that all sides have equal length
    3. Verify that adjacent sides form a 90 degree angle
    """
    # Sort points to get a standard ordering
    points = sorted([(p.x, p.y) for p in [p1, p2, p3, p4]])
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    x4, y4 = points[3]
    
    # Calculate side lengths
    a1 = sqrt((x1-x2)**2 + (y1-y2)**2)
    a2 = sqrt((x4-x2)**2 + (y4-y2)**2)
    a3 = sqrt((x4-x3)**2 + (y4-y3)**2)
    a4 = sqrt((x1-x3)**2 + (y1-y3)**2)
    
    # All sides must be equal and non-zero, and angles must be 90 degrees
    sides_equal = a1 == a2 == a3 == a4 and a1 != 0 and a4 != 0
    
    # Check angle is 90 degrees using the law of sines
    if sides_equal:
        angle_diff = abs(degrees(asin((y2-y1)/a1) - asin((y3-y1)/a4)))
        right_angle = abs(abs(angle_diff) - 90) <= 1e-8
        return right_angle
    
    return False

def is_rectangle(p1, p2, p3, p4):
    """
    Check if 4 points form a rectangle
    Steps:
    1. Sort the points to get a predictable ordering
    2. Verify that opposite sides have equal length
    3. Verify that adjacent sides form a 90 degree angle
    """
    # Sort points to get a standard ordering
    points = sorted([(p.x, p.y) for p in [p1, p2, p3, p4]])
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    x4, y4 = points[3]
    
    # Calculate side lengths
    a1 = sqrt((x1-x2)**2 + (y1-y2)**2)
    a2 = sqrt((x4-x2)**2 + (y4-y2)**2)
    a3 = sqrt((x4-x3)**2 + (y4-y3)**2)
    a4 = sqrt((x1-x3)**2 + (y1-y3)**2)
    
    # Opposite sides must be equal and non-zero, and angles must be 90 degrees
    opposite_sides_equal = a1 == a3 and a2 == a4 and a1 != 0 and a4 != 0
    
    # Check angle is 90 degrees using the law of sines
    if opposite_sides_equal:
        angle_diff = abs(degrees(asin((y2-y1)/a1) - asin((y3-y1)/a4)))
        right_angle = abs(abs(angle_diff) - 90) <= 1e-8
        return right_angle
    
    return False

# Read the 8 points
points = []
for i in range(8):
    x, y = map(int, input().split())
    points.append(Point(x, y))

# Try all possible combinations of 4 points for the square
found = False
for i in range(5):
    for j in range(i+1, 6):
        for k in range(j+1, 7):
            for l in range(k+1, 8):
                # Check if these 4 points form a square
                if is_square(points[i], points[j], points[k], points[l]):
                    # Get the remaining 4 points for the rectangle
                    remaining = []
                    remaining_indices = []
                    for m in range(8):
                        if m not in [i, j, k, l]:
                            remaining.append(points[m])
                            remaining_indices.append(m+1)
                    
                    # Check if remaining points form a rectangle
                    if is_rectangle(remaining[0], remaining[1], remaining[2], remaining[3]):
                        print("YES")
                        print(i+1, j+1, k+1, l+1)
                        print(*remaining_indices)
                        found = True
                        break
            if found:
                break
        if found:
            break
    if found:
        break

if not found:
    print("NO")