#!/usr/bin/env python3
from library import is_power_of_two_minus_one

def solve():
    n = int(input())
    
    # Try different values of k starting from 2
    # We need to find x such that x * (2^k - 1) = n
    # So x = n / (2^k - 1)
    
    k = 2
    while True:
        denominator = (1 << k) - 1  # 2^k - 1
        if n % denominator == 0:
            return n // denominator
        k += 1
        
        # Safety check to avoid infinite loop
        if k > 32:  # 2^32 - 1 > 10^9
            break
    
    return -1  # Should never happen based on problem constraints

t = int(input())
for _ in range(t):
    print(solve())