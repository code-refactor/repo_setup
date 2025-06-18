#!/usr/bin/env python3
from library import is_prime, mod_pow, mod_inverse

def solve():
    n = int(input())
    
    # Special cases
    if n == 1:
        print('YES')
        print(1)
        return
    
    if n == 4:
        print('YES')
        print(1)
        print(3)
        print(2)
        print(4)
        return
    
    # Check if n is prime (solution only exists for prime n and special cases)
    if not is_prime(n):
        print('NO')
        return
    
    # For prime n, construct the sequence
    print('YES')
    print(1)  # First element is always 1
    
    # For j from 2 to n-1, calculate j * (j-1)^(n-2) mod n
    for j in range(2, n):
        # Using modular inverse: (j-1)^(n-2) = (j-1)^(-1) mod n
        inverse_j_minus_1 = mod_inverse(j - 1, n)
        result = (j * inverse_j_minus_1) % n
        print(result)
    
    print(n)  # Last element is always n

solve()