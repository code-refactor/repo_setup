#!/usr/bin/env python3
from library import is_prime, find_smallest_prime_factor

n = int(input())

if is_prime(n):
    print(1)
else:
    if n % 2 == 0:
        # If n is even, the smallest prime divisor is 2
        # We can keep subtracting 2 until we reach 0
        print(n // 2)
    else:
        # If n is odd, we find the smallest prime divisor
        # After subtracting it once, the result becomes even
        # Then we can keep subtracting 2 until we reach 0
        smallest_prime = find_smallest_prime_factor(n)
        print(((n - smallest_prime) // 2) + 1)