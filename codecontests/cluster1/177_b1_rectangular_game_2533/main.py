#!/usr/bin/env python3

from library import find_smallest_prime_factor

def solve():
    n = int(input())
    result = n + 1  # Start with n, then add 1 for the final step (when we reach 1)
    
    # Keep factoring by smallest prime factors
    while True:
        # Find the smallest prime factor
        smallest_factor = find_smallest_prime_factor(n)
        
        # If n is prime, we're done (no more factorization possible)
        if smallest_factor == n:
            break
            
        # Add the quotient (which is the number of pebbles we keep in the row)
        quotient = n // smallest_factor
        result += quotient
        
        # Continue with the quotient (not the smallest factor!)
        n = quotient
    
    print(result)

solve()