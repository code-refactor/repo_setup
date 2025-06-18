#!/usr/bin/env python3
from library import unique_prime_factors, mod_pow

MOD = 1000000007

def solve():
    x, n = map(int, input().split())
    
    # Get unique prime factors of x
    prime_factors = unique_prime_factors(x)
    
    result = 1
    for p in prime_factors:
        # Calculate the total power by summing contributions
        temp_n = n
        while temp_n > 0:
            result = (result * mod_pow(p, temp_n // p, MOD)) % MOD
            temp_n //= p
    
    return result

print(solve())

