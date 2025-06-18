#!/usr/bin/env python3

from library import Point, are_collinear, are_collinear_triplet

n = int(input())
points = []
for _ in range(n):
    a, b = map(int, input().split())
    points.append((a, b))

# If n <= 4, we can always place points on two lines
if n <= 4:
    print("YES")
    exit()

def can_place_on_two_lines():
    # Try every possible pair of points to define the first line
    for i in range(n):
        for j in range(i+1, n):
            # Points on the first line (defined by points[i] and points[j])
            line1_points = []
            # Points not on the first line
            remaining_points = []
            
            x1, y1 = points[i]
            x2, y2 = points[j]
            
            # Check which points are on the first line
            for k in range(n):
                x3, y3 = points[k]
                if are_collinear_triplet(x1, y1, x2, y2, x3, y3):
                    line1_points.append(k)
                else:
                    remaining_points.append(k)
            
            # If all points are on the first line, we're done
            if len(remaining_points) == 0:
                return True
                
            # If only one point is not on the first line, it defines a line by itself
            if len(remaining_points) == 1:
                return True
                
            # Check if remaining points are collinear (on the second line)
            x1, y1 = points[remaining_points[0]]
            x2, y2 = points[remaining_points[1]]
            
            all_collinear = True
            for k in range(2, len(remaining_points)):
                x3, y3 = points[remaining_points[k]]
                if not are_collinear_triplet(x1, y1, x2, y2, x3, y3):
                    all_collinear = False
                    break
            
            if all_collinear:
                return True
    
    return False

if can_place_on_two_lines():
    print("YES")
else:
    print("NO")