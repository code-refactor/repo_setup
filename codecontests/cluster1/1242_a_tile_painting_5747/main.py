#!/usr/bin/env python3
from library import find_divisors, gcd

def solve():
    n = int(input())
    
    if n < 3:
        return n
    
    # Find all divisors greater than 1 and less than n
    divisors = find_divisors(n)
    proper_divisors = [d for d in divisors if 1 < d < n]
    
    if len(proper_divisors) == 0:
        # n is prime
        return n
    
    # Find GCD of all proper divisors
    result_gcd = proper_divisors[0]
    for d in proper_divisors[1:]:
        result_gcd = gcd(result_gcd, d)
    
    return result_gcd

print(solve())