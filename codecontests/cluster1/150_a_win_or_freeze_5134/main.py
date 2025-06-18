#!/usr/bin/env python3

from library import prime_factorization

def solve():
    n = int(input())
    
    # Special case: if n is 1, player 1 wins immediately (no moves possible)
    if n == 1:
        print(1)
        print(0)
        return
    
    # Get prime factorization of n
    prime_factors = prime_factorization(n)
    
    # Game theory analysis:
    # - If n has 1 prime factor (i.e., n is a prime power), player 1 wins (no non-trivial divisors)
    # - If n has exactly 2 prime factors, player 2 wins (player 1 can only move to a prime power)
    # - If n has 3+ prime factors, player 1 wins (can move to a number with 2 prime factors)
    
    if len(prime_factors) == 1:
        # n is a prime power, player 1 wins immediately
        print(1)
        print(0)
    elif len(prime_factors) == 2:
        # n has exactly 2 prime factors, player 2 wins
        print(2)
    else:
        # n has 3 or more prime factors, player 1 wins
        # Winning move: multiply any two prime factors to get a number with exactly 2 prime factors
        winning_move = prime_factors[0] * prime_factors[1]
        print(1)
        print(winning_move)

solve()