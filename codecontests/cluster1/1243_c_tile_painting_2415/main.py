#!/usr/bin/env python3
from library import unique_prime_factors

n = int(input())
p = unique_prime_factors(n)

if len(p) == 1:
    print(p[0])
else:
    print(1)