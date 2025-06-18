#!/usr/bin/env python3
from library import unique_prime_factors, is_prime

def get_smallest_prime_factor(n):
    """Get the smallest prime factor of n."""
    if n <= 1:
        return n
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return i
    return n

def is_prime_power(n):
    """Check if n is a prime power (p^k where p is prime and k >= 1)."""
    if n <= 1:
        return False
    
    # Get unique prime factors
    prime_factors = unique_prime_factors(n)
    
    # A prime power has exactly one unique prime factor
    return len(prime_factors) == 1

def solve():
    n = int(input())
    
    # Find all prime powers from 2 to n, grouped by prime
    prime_powers = []
    
    # Find all primes up to n
    primes = []
    for i in range(2, n + 1):
        if is_prime(i):
            primes.append(i)
    
    # For each prime, find all its powers <= n
    for p in primes:
        power = p
        while power <= n:
            prime_powers.append(power)
            power *= p
    
    print(len(prime_powers))
    if prime_powers:
        print(' '.join(map(str, prime_powers)))
    else:
        print()

solve()
