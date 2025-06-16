#!/usr/bin/env python3
from library import get_divisors, gcd

n = int(input())
if n < 3:
    print(n)
else:
    divisors = get_divisors(n)[1:-1]  # Exclude 1 and n
    if not divisors:
        print(n)
    else:
        g = divisors[0]
        for d in divisors[1:]:
            g = gcd(g, d)
        print(g)
    



    
    