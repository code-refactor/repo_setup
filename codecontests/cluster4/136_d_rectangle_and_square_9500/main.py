#!/usr/bin/env python3

from library import Point, is_square, is_rectangle
import itertools
import sys

# Read the 8 points
points = [None]  # 1-indexed points
for i in range(8):
    x, y = map(int, input().split())
    points.append(Point(x, y))

# Try all possible combinations of 4 points for the square
for square_indices in itertools.combinations(range(1, 9), 4):
    # Get the points for the square
    square_points = [points[i] for i in square_indices]
    
    # Get the remaining points for the rectangle
    rect_indices = [i for i in range(1, 9) if i not in square_indices]
    rect_points = [points[i] for i in rect_indices]
    
    # Check if square_points form a square and rect_points form a rectangle
    if is_square(*square_points) and is_rectangle(*rect_points):
        print("YES")
        print(' '.join(map(str, square_indices)))
        print(' '.join(map(str, rect_indices)))
        sys.exit(0)
    
    # Check if rect_points form a square and square_points form a rectangle
    if is_square(*rect_points) and is_rectangle(*square_points):
        print("YES")
        print(' '.join(map(str, rect_indices)))
        print(' '.join(map(str, square_indices)))
        sys.exit(0)

print("NO")