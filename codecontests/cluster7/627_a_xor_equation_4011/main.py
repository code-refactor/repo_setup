#!/usr/bin/env python3

from library import read_ints

# Read input: s (sum) and x (XOR)
s, x = read_ints()

# Check if there's a solution
if s < x or (s - x) & 1:
    print(0)
    exit(0)
    
# Calculate u (the number to add to get sum s) and d (the xor value x)
u, d = (s - x) // 2, x
res = 1

# Check bit by bit compatibility
while u or d:
    uu, dd = u & 1, d & 1
    # If both bits are 1, impossible case
    if uu and dd:
        res *= 0
    # If u bit is 0 and d bit is 1, we have 2 choices
    elif uu == 0 and dd == 1:
        res *= 2
    u, d = u >> 1, d >> 1

# Special case: if s == x, remove 2 cases (all zeros and all ones)
if s == x:
    res = max(0, res - 2)
    
print(res)