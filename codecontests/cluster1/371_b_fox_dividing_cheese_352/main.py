#!/usr/bin/env python3
from library import prime_factorization, factor_counter

def count_factor_power(n, factor):
    """Count how many times a factor divides n."""
    count = 0
    while n % factor == 0:
        count += 1
        n //= factor
    return count

def remove_factors(n, factors):
    """Remove all instances of given factors from n."""
    result = n
    for factor in factors:
        while result % factor == 0:
            result //= factor
    return result

def solve():
    a, b = map(int, input().split())
    
    # If already equal
    if a == b:
        return 0
    
    # Count powers of 2, 3, 5 in both numbers
    a_pow_2 = count_factor_power(a, 2)
    a_pow_3 = count_factor_power(a, 3)
    a_pow_5 = count_factor_power(a, 5)
    
    b_pow_2 = count_factor_power(b, 2)
    b_pow_3 = count_factor_power(b, 3)
    b_pow_5 = count_factor_power(b, 5)
    
    # Remove all powers of 2, 3, 5 to get the core numbers
    a_core = remove_factors(a, [2, 3, 5])
    b_core = remove_factors(b, [2, 3, 5])
    
    # If core numbers are different, impossible to make equal
    if a_core != b_core:
        return -1
    
    # Return sum of absolute differences in powers
    return abs(a_pow_2 - b_pow_2) + abs(a_pow_3 - b_pow_3) + abs(a_pow_5 - b_pow_5)

print(solve())
