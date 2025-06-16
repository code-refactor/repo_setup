#!/usr/bin/env python3

from library import normalize_fraction

n, x0, y0 = map(int, input().split())
slopes = {} # key: (num, den), val: count

for i in range(n):
    x, y = map(int, input().split())
    num = y - y0
    den = x - x0
    
    if den == 0:
        slope = "inf"
    else:
        slope = normalize_fraction(num, den)
    
    if slope in slopes:
        slopes[slope] += 1
    else:
        slopes[slope] = 1
        
print(len(slopes))
    