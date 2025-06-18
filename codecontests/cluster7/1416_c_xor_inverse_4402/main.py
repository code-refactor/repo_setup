#!/usr/bin/env python3

from library import read_int, read_array

n = read_int()
arr = read_array()

total_inversions = 0  # Count of inversions we need to fix
optimal_xor = 0       # The optimal XOR value

# Process bit by bit from least significant to most significant
multiplier = 1  # 2^i for current bit position
for bit_pos in range(32):  # 32 bits in an integer
    # Count inversions for this bit position
    # hash0 tracks numbers with bit=0, hash1 tracks numbers with bit=1
    hash0 = {}  # Maps number//2 -> count of numbers with bit=0
    hash1 = {}  # Maps number//2 -> count of numbers with bit=1
    
    # Count inversions if we don't flip this bit
    inv_no_flip = 0
    # Count inversions if we flip this bit
    inv_with_flip = 0
    
    for num in arr:
        bit = num % 2  # Current bit value (0 or 1)
        prefix = num // 2  # The prefix (higher bits)
        
        # Count inversions
        if bit == 0 and prefix in hash1:
            # If we have seen numbers with same prefix but bit=1,
            # they would be out of order if we don't flip
            inv_no_flip += hash1[prefix]
        
        if bit == 1 and prefix in hash0:
            # If we have seen numbers with same prefix but bit=0,
            # they would be out of order if we flip
            inv_with_flip += hash0[prefix]
        
        # Update hash tables
        if bit == 1:
            hash1[prefix] = hash1.get(prefix, 0) + 1
        else:
            hash0[prefix] = hash0.get(prefix, 0) + 1
    
    # Choose the option with fewer inversions
    if inv_no_flip <= inv_with_flip:
        total_inversions += inv_no_flip
    else:
        total_inversions += inv_with_flip
        optimal_xor += multiplier  # Set this bit in the optimal XOR
    
    # Prepare for next bit
    multiplier *= 2
    
    # Shift all numbers right by 1 for next bit
    for i in range(n):
        arr[i] = arr[i] // 2

print(total_inversions, optimal_xor)