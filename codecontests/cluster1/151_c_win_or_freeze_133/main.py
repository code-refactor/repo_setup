#!/usr/bin/env python3

def prime_factorize(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    if n > 2:
        factors.append(n)
    return factors

import sys
line = sys.stdin.readline()
N = int(line)
factor = prime_factorize(N)

if len(factor) == 2: print(2)
else:
    print(1)
    if len(factor) <= 1: print(0)
    else: print(factor[0] * factor[1])