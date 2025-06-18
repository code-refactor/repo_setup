#!/usr/bin/env python3
from library import find_divisors

def solve():
    n, k = map(int, input().split())
    
    # Find all divisors using the library function
    divisors = find_divisors(n)
    
    # Check if k-th divisor exists
    if k > len(divisors):
        print(-1)
    else:
        print(divisors[k-1])  # k-th divisor (0-indexed)

solve()