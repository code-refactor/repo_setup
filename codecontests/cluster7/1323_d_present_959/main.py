#!/usr/bin/env python3

from library import read_int, read_array

def solve():
    n = read_int()
    a = read_array()
    
    # Find the maximum bit length in the array
    b = max(a).bit_length()
    res = 0
    vals = a
    
    # Process each bit position
    for i in range(b + 1):
        # Bit masks for current position
        b2 = 2 << i  # 2^(i+1)
        b1 = 1 << i  # 2^i
        
        # Partition array by whether the i-th bit is set
        a0 = [num for num in a if num & b1 == 0]
        a1 = [num for num in a if num & b1]
        
        # Combine and get modulo values
        a = a0 + a1
        vals = [num % b2 for num in a]
        
        # Count pairs that will have i-th bit set in their XOR
        cnt = 0
        x1, x2, y1 = n - 1, n - 1, n - 1
        
        for j, v in enumerate(vals):
            # First range: [b1-v, b2-v-1]
            while x1 > -1 and vals[x1] >= b1 - v:
                x1 -= 1
            while y1 > -1 and vals[y1] > b2 - v - 1:
                y1 -= 1
                
            x, y = x1 + 1, y1 + 1
            cnt += y - x
            if x <= j < y:
                cnt -= 1  # Don't count the pair with itself

            # Second range: [b2+b1-v, infinity)
            while x2 > -1 and vals[x2] >= b2 + b1 - v:
                x2 -= 1
                
            x, y = x2 + 1, n
            cnt += y - x
            if x <= j < y:
                cnt -= 1  # Don't count the pair with itself

        # Add to result if there are an odd number of pairs
        res += b1 * (cnt // 2 % 2)
        
    return res

print(solve())