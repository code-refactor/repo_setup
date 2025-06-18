#!/usr/bin/env python3

from library import read_int, read_ints

n = read_int()
parent = [0] + [x-1 for x in read_ints()]  # Convert to 0-indexed
citizen = read_ints()  # Number of citizens in each city

# Count leaf nodes - cities with no children
sz = [1] * n  # Initialize all cities as leaf nodes
for i in range(1, n):
    sz[parent[i]] = 0  # Mark non-leaf nodes

# Process from leaf to root (bottom-up)
for i in range(n-1, 0, -1):
    # Propagate citizens and leaf count upwards
    citizen[parent[i]] += citizen[i]
    sz[parent[i]] += sz[i]

# Calculate the minimum answer
ans = 0
for i in range(n):
    # Number of citizens per leaf city in this subtree
    citizens_per_leaf = citizen[i] // sz[i]
    if citizen[i] % sz[i] != 0:
        # If distribution isn't even, we need one more citizen for some leaves
        citizens_per_leaf += 1
    
    ans = max(ans, citizens_per_leaf)

print(ans)