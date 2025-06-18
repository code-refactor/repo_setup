#!/usr/bin/env python3

from library import read_ints

# Read input: s (sum) and x (XOR)
s, x = read_ints()

# Check if a solution exists
if x > s or (s-x) % 2 != 0:
    print(0)
else:
    mask = 1
    res = 1
    bit = 0
    # Calculate the added value for each variable
    ND = (s-x) // 2
    flag = False
    
    # Check bit by bit
    while bit < 50:  # Enough for 64-bit integers
        # If x has a 1 bit here, we have two choices
        if (mask & x) > 0:
            res *= 2
        # If both x and ND have 1 in the same position, impossible
        if mask & x > 0 and ND & mask > 0:
            flag = True
            break
        mask *= 2
        bit += 1
    
    # Special case: if s == x, remove two invalid solutions
    if s == x:
        res -= 2
    if flag:
        res = 0
    print(res)
    