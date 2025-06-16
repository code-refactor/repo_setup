#!/usr/bin/env python3
from library import prime_factorize

n = int(input())
p = list(set(prime_factorize(n)))

if len(p) == 1:
    print(p[0])
else:
    print(1)