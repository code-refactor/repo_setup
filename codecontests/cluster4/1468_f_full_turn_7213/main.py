#!/usr/bin/env python3

from library import Point, get_slope_from_coords, setup_io
from math import gcd
from collections import Counter

input = setup_io()

def solve_testcase():
    n = int(input())
    vector_counts = Counter()
    
    for _ in range(n):
        x, y, u, v = map(int, input().split())
        
        # Calculate vector from starting point to ending point
        dx, dy = u - x, v - y
        
        # Normalize the vector
        if dx == 0:
            vector_counts[(0, 1 if dy > 0 else -1)] += 1
        elif dy == 0:
            vector_counts[(1 if dx > 0 else -1, 0)] += 1
        else:
            g = gcd(abs(dx), abs(dy))
            dx, dy = dx // g, dy // g
            vector_counts[(dx, dy)] += 1
    
    # Count pairs of vectors that can form a full turn (opposite directions)
    total_pairs = 0
    for vector, count in vector_counts.items():
        opposite_vector = (-vector[0], -vector[1])
        if opposite_vector in vector_counts:
            total_pairs += count * vector_counts[opposite_vector]
    
    # Each pair is counted twice, so divide by 2
    return total_pairs // 2

t = int(input())
for _ in range(t):
    print(solve_testcase())