#!/usr/bin/env python3
from library import prime_factorize, mod_pow, MOD

x, n = map(int, input().split())

prime_factors = list(set(prime_factorize(x)))
mul = 1
for d in prime_factors:
    nn = n
    while nn > 0:
        mul = (mul * mod_pow(d, nn // d, MOD)) % MOD
        nn = nn // d

print(mul)

