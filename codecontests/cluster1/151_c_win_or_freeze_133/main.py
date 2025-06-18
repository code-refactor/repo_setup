#!/usr/bin/env python3

from library import prime_factorization

def solve():
    N = int(input())
    
    # Get prime factorization of N (with repetition)
    prime_factors = prime_factorization(N)
    
    # Game theory analysis:
    # - If N has 1 prime factor (total, with repetition), i.e., N is a prime power, player 1 wins (no non-trivial divisors)
    # - If N has exactly 2 prime factors (total, with repetition), player 2 wins 
    # - If N has 3+ prime factors (total, with repetition), player 1 wins
    
    if len(prime_factors) == 2:
        # N has exactly 2 prime factors (with repetition), player 2 wins
        print(2)
    else:
        # N has 1 or 3+ prime factors (with repetition), player 1 wins
        print(1)
        if len(prime_factors) <= 1:
            # N is 1 or a prime power, no moves possible
            print(0)
        else:
            # N has 3+ prime factors, winning move: multiply first two prime factors
            winning_move = prime_factors[0] * prime_factors[1]
            print(winning_move)

solve()