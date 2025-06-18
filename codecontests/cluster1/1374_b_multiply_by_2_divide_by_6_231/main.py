#!/usr/bin/env python3
from library import factor_counter

def solve():
    n = int(input())
    
    # Base case
    if n == 1:
        return 0
    
    # Get prime factorization
    factors = factor_counter(n)
    
    # Only powers of 2 and 3 are allowed (since 6 = 2 * 3)
    for prime in factors:
        if prime != 2 and prime != 3:
            return -1
    
    # Count powers of 2 and 3
    power_of_2 = factors.get(2, 0)
    power_of_3 = factors.get(3, 0)
    
    # To reach 1, we need equal powers of 2 and 3 at the end
    # We can multiply by 2 (add power of 2) or divide by 6 (subtract one power of 2 and 3)
    # If power_of_2 > power_of_3, it's impossible
    if power_of_2 > power_of_3:
        return -1
    
    # We need to make powers of 2 equal to powers of 3
    # Each multiplication by 2 adds 1 to power of 2
    # Each division by 6 subtracts 1 from both powers
    # Final answer: 2 * power_of_3 - power_of_2
    return 2 * power_of_3 - power_of_2

def main():
    t = int(input())
    for _ in range(t):
        print(solve())

if __name__ == "__main__":
    main()
