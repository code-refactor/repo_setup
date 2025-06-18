#!/usr/bin/env python3
from library import factor_counter

def solve():
    n = int(input())
    
    # Get prime factorization
    factors = factor_counter(n)
    
    # If n is prime, we can only have a sequence of length 1
    if not factors or (len(factors) == 1 and list(factors.values())[0] == 1):
        print(1)
        print(n)
        return
    
    # Find the prime with maximum power
    max_power = 0
    best_prime = 2
    for prime, power in factors.items():
        if power > max_power:
            max_power = power
            best_prime = prime
    
    # Build sequence: prime repeated (max_power-1) times, then the remaining factor
    sequence_length = max_power
    remaining_factor = n // (best_prime ** (max_power - 1))
    
    print(sequence_length)
    
    # Print the sequence
    result = [best_prime] * (max_power - 1) + [remaining_factor]
    print(' '.join(map(str, result)))

def main():
    t = int(input())
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
