#!/usr/bin/env python3

from library import Point, get_slope_from_coords
from math import gcd

def normalize_rational(num, den):
    """
    Convert a fraction to its simplest form with consistent sign representation
    """
    # Handle sign: make denominator positive, numerator holds the sign
    if den < 0:
        num, den = -num, -den
    
    # Simplify the fraction
    if num != 0:
        g = gcd(abs(num), abs(den))
        num //= g
        den //= g
    elif den != 0:
        den = 1
    
    return (num, den)

# Read input
n, m = map(int, input().split())
flamingos = []

for _ in range(m):
    x, y = map(int, input().split())
    flamingos.append((x, y))

# Initialize maximum hits array for each binocular
max_hits = [1] * (n + 1)
max_hits[0] = 0  # No binocular at position 0

# Map to store lines and the points on them
line_to_points = {}

# Calculate lines connecting each pair of flamingos
for i in range(m):
    for j in range(i + 1, m):  # Only check each pair once
        x1, y1 = flamingos[i]
        x2, y2 = flamingos[j]
        
        # Calculate the slope and y-intercept of the line
        dx = x2 - x1
        dy = y2 - y1
        
        # Skip horizontal lines (they don't intersect the x-axis at a binocular)
        if dy == 0:
            continue
        
        # Calculate normalized slope for consistent representation
        slope = normalize_rational(dy, dx)
        
        # Calculate x-intercept with the x-axis (y=0)
        # From the line equation: y = mx + b
        # At y=0: 0 = mx + b => x = -b/m
        # Using point-slope form: y - y1 = m(x - x1)
        # At y=0: -y1 = m(x - x1) => x = x1 - y1/m = x1 - y1*dx/dy
        
        # Compute c' = y1*dx - x1*dy (rearranged from the equation)
        c_prime = y1 * dx - x1 * dy
        
        # Calculate x-intercept: x = -c'/dy
        x_intercept = -c_prime / dy
        
        # Use the slope and x-intercept as a key for the line
        line_key = (slope, x_intercept)
        
        # If we've already seen this line, add these points to it
        if line_key in line_to_points:
            points = line_to_points[line_key]
            points.add(i)
            points.add(j)
            continue
        
        # If the line passes through a binocular position (integer x-intercept in range [1,n])
        if int(x_intercept) == x_intercept and 1 <= x_intercept <= n:
            # Create a new entry for this line
            line_to_points[line_key] = {i, j}

# Update maximum hits for each binocular
for line, points in line_to_points.items():
    x_intercept = int(line[1])
    max_hits[x_intercept] = max(max_hits[x_intercept], len(points))

# Calculate the total maximum number of flamingos visible
print(sum(max_hits))