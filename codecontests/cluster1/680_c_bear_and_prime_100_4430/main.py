#!/usr/bin/env python3

# 680C - Bear and Prime 100
from library import is_prime

def query(num):
    """Ask if num is a divisor of the hidden number."""
    print(num)
    sys.stdout.flush()
    response = input().strip()
    return "yes" in response.lower()

def solve():
    """
    Interactive solution to determine if a hidden number [2,100] is prime or composite.
    We can ask up to 20 queries about divisors.
    """
    # Strategy: Check small primes first, then handle special cases
    small_primes = [2, 3, 5, 7]
    divisors_found = []
    
    # Check divisibility by small primes
    for p in small_primes:
        if query(p):
            divisors_found.append(p)
    
    # If multiple small prime divisors, definitely composite
    if len(divisors_found) >= 2:
        print("composite")
        return
    
    # If exactly one small prime divisor
    if len(divisors_found) == 1:
        p = divisors_found[0]
        
        # Check for higher powers of this prime
        power = p * p
        while power <= 100:
            if query(power):
                print("composite")
                return
            power *= p
        
        # Check if other primes divide the number
        larger_primes = [q for q in range(11, 50) if is_prime(q)]
        for q in larger_primes:
            if p * q > 100:  # No point checking if product exceeds 100
                break
            if query(q):
                print("composite")
                return
        
        # Only one prime factor found
        print("prime")
        return
    
    # No small prime divisors found
    # Check larger primes (11-97)
    larger_primes = [p for p in range(11, 100) if is_prime(p)]
    for p in larger_primes:
        if query(p):
            print("prime")  # If divisible by a prime > 7, it must be that prime
            return
    
    # Check perfect squares of small primes
    squares = [4, 9, 25, 49]  # 2^2, 3^2, 5^2, 7^2
    for sq in squares:
        if query(sq):
            print("composite")
            return
    
    # If we reach here, the number has no small divisors
    print("prime")

solve()
