#!/usr/bin/env python3
from library import is_prime, prime_factorize

n = int(input())
if is_prime(n):
    print(1)
else:
    if n % 2:
        factors = prime_factorize(n)
        print(((n - factors[0]) // 2) + 1)
    else:
        print(n // 2)