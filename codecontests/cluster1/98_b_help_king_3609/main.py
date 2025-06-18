#!/usr/bin/env python3

# 98B - Help King  
from library import gcd
from fractions import Fraction

def solve():
    n = int(input())
    
    # Count powers of 2 in n and remove them
    L = 0
    while n % 2 == 0:
        n //= 2
        L += 1
    
    # If n becomes 1 (was a power of 2), answer is L
    if n == 1:
        print(f'{L}/1')
        return
    
    # Find multiplicative order of 2 modulo n
    s = 1  # s will be 2^m 
    t = 1  # t tracks 2^i mod n
    
    for i in range(n):
        t = (t * 2) % n
        s *= 2
        if t == 1:
            m = i + 1
            break
    
    # Calculate expected cost using the rejection sampling approach
    r = s        # remaining outcomes to handle
    t = s * n    # current threshold 
    i = L        # current tree depth
    ans = 0      # total expected cost
    
    while r > 1:
        i += 1
        t //= 2
        if r - t > 0:
            ans += i * t
            r -= t
    
    # Final expected value calculation
    numerator = ans + m
    denominator = s - 1
    
    result = Fraction(numerator, denominator)
    print(result)

solve()
