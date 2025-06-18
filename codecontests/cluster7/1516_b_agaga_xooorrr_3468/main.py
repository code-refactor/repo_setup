#!/usr/bin/env python3

from library import read_int, read_array, xor_array, yes_no

for _ in range(read_int()):
    n = read_int()
    a = read_array()
    
    # Calculate XOR of entire array
    r = xor_array(a)
    
    if not r:
        yes_no(True)
    else:
        t = 0
        i = 0
        s = 0
        
        while i < len(a) and t < 2:
            s ^= a[i]
            if s == r:
                t += 1
                s = 0
            i += 1
            
        yes_no(t == 2)