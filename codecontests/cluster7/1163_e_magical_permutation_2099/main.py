#!/usr/bin/env python3

import math
from library import read_int, read_array

def size(k):
    """Calculate log2 of k (position of the most significant bit)"""
    return int(math.log2(k))

def v2(k):
    """Calculate trailing zeros in binary representation of k"""
    if k % 2 == 1:
        return 0
    else:
        return 1 + v2(k // 2)

n = read_int()
s = read_array()
s.sort()  # Sort input array

used = []  # Numbers we include in our basis
use = 0    # Count of numbers in our basis
found = {0: 1}  # Set of representable numbers
good = 0  # Size of the largest valid basis

# Try to build a linearly independent basis over GF(2)
for num in s:
    big = size(num)  # Position of the most significant bit
    
    if num not in found:
        used.append(num)
        use += 1
        
        # Add new combinations by XORing with existing numbers
        new = []
        for existing in found:
            new.append(existing ^ num)
        
        for new_num in new:
            found[new_num] = 1
        
        # If we have enough numbers for a basis of size big+1
        if use == big + 1:
            good = use

# If no valid basis found
if good == 0:
    print(0)
    print(0)
else:
    # Construct the permutation
    useful = used[:good]
    perm = ["0"]
    curr = 0
    
    # For each number in the permutation
    for i in range(2**good - 1):
        # XOR with the appropriate basis element
        curr ^= useful[v2(i + 1)]
        perm.append(str(curr))
    
    print(good)
    print(" ".join(perm))