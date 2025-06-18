#!/usr/bin/env python3

from library import gcd, find_divisors
from functools import reduce

def solve():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    # Calculate GCD of all (ai - 1) values
    # This represents the constraint that any valid starting pair must satisfy
    g = reduce(gcd, [x - 1 for x in a])
    
    answer = 0
    
    def process(x):
        """Count valid pairs (i, j) where gcd(i-1, j-1) = x"""
        nonlocal answer
        # Only odd divisors contribute to the count
        if x % 2 == 0:
            return
        
        # For each power of 2 times x, count valid pairs
        for i in range(30):  # 2^30 > 10^9, so this covers all cases
            v = (2 ** i) * x
            if v > m:
                break
            # Count pairs (i, j) where i-1 = v-1 and j > i
            # This means i = v and j can be v+1, v+2, ..., m
            answer += m - v
    
    # Find all divisors of g and process each
    divisors = find_divisors(g)
    for divisor in divisors:
        process(divisor)
    
    print(answer)

solve()
