#!/usr/bin/env python3

from library import read_ints

u, v = read_ints()

if u > v:
    print(-1)
elif u == 0 and v == 0:
    print(0)
elif u == v:
    print(1, end=' ')
    print(u)
else:
    # Check if we can decompose v into u + 2*k for some k
    # where k ^ k = 0 and k + k = diff
    diff = v - u
    
    # If diff is odd, it can't be expressed as 2*k
    if diff % 2 != 0:
        print(-1)
    else:
        a, b = u, diff // 2
        
        # If a and b share any bit positions, 
        # we need to decompose b into parts that don't share bits with a
        if a & b == 0:  # No shared bits
            if b == 0:  # v == u case
                print(1, end=' ')
                print(u)
            else:
                # Print without newline between count and values
                print(2, end=' ')
                print(a | b, b)
        else:
            # Need to split into 3 numbers
            print(3, end=' ')
            print(a, b, b)