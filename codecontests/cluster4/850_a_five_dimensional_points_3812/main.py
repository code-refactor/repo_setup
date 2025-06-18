#!/usr/bin/env python3

from library import Point
import math

# Function to calculate dot product of vectors from a to b and a to c in 5D
def dot_product_5d(a, b, c):
    """Calculate dot product of vectors (b-a) and (c-a) in 5D space"""
    result = 0
    for m in range(5):
        result += (b[m] - a[m]) * (c[m] - a[m])
    return result

# Read input
n = int(input())
points = []
for _ in range(n):
    points.append(list(map(int, input().split())))

# Early optimization for large inputs (not needed for correctness)
if n > 11:
    print(0)
else:
    # Check each point if it's good
    good_points = []
    
    for i in range(n):
        is_good = True
        
        # Try all pairs of other points to see if they form an acute angle with current point
        for j in range(n):
            if j == i:
                continue
                
            for k in range(j+1, n):
                if k == i:
                    continue
                
                # Calculate dot product between vectors from i to j and i to k
                # If dot product > 0, the angle is acute (less than 90°)
                if dot_product_5d(points[i], points[j], points[k]) > 0:
                    is_good = False
                    break
            
            if not is_good:
                break
        
        # If the point is good, add its index (1-indexed) to the result
        if is_good:
            good_points.append(i + 1)
    
    # Output results
    print(len(good_points))
    for point in good_points:
        print(point)