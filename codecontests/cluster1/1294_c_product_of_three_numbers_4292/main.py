#!/usr/bin/env python3
from library import find_divisors

def solve():
    n = int(input())
    original_n = n
    
    # Find first factor
    a = None
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            a = i
            break
    
    if a is None:
        return "NO"  # n is prime or 1
    
    # Find second factor from the remaining number
    remaining = n // a
    b = None
    for i in range(2, int(remaining**0.5) + 1):
        if remaining % i == 0 and i != a:
            b = i
            break
    
    if b is None:
        return "NO"  # remaining is prime or has no valid factor
    
    # Calculate c
    if original_n % (a * b) != 0:
        return "NO"
    
    c = original_n // (a * b)
    
    # Check if c is valid (>= 2 and distinct from a and b)
    if c < 2 or c == a or c == b:
        return "NO"
    
    return f"YES\n{a} {b} {c}"

t = int(input())
for _ in range(t):
    print(solve())