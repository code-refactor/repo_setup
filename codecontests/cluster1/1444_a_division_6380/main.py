#!/usr/bin/env python3
from library import factor_counter, unique_prime_factors

def solve():
    p, q = map(int, input().split())
    
    # If p is not divisible by q, then p itself is the answer
    if p % q != 0:
        return p
    
    # Get prime factors of q
    q_factors = factor_counter(q)
    
    # For each prime factor of q, we need to reduce its power in p
    # to make the result not divisible by q
    min_divisor = float('inf')
    
    for prime in q_factors:
        q_power = q_factors[prime]  # Power of prime in q
        
        # Count power of this prime in p
        p_power = 0
        temp_p = p
        while temp_p % prime == 0:
            p_power += 1
            temp_p //= prime
        
        # If p has less power of this prime than q, p is not divisible by q
        if p_power < q_power:
            continue
            
        # We need to reduce the power of this prime in p
        # The minimum factor to divide by is prime^(p_power - q_power + 1)
        divisor = prime ** (p_power - q_power + 1)
        min_divisor = min(min_divisor, divisor)
    
    return p // min_divisor

def main():
    t = int(input())
    for _ in range(t):
        print(solve())

if __name__ == "__main__":
    main()