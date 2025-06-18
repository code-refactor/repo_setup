#!/usr/bin/env python3

# 99D - Help King
  
from library import gcd

def print_fraction(a, b):
    """Print fraction in the required format"""
    print(f"{int(a)}/{int(b)}")

def solve():
    n = int(input())
    
    # Count and remove powers of 2 from n
    pre = 0
    while n > 1 and n % 2 == 0:
        pre += 1
        n //= 2
    
    # If n becomes 1, it was a power of 2
    if n == 1:
        print_fraction(pre, 1)
        return
    
    # Find the binary representation of fractions 1/n, 2/n, 3/n, ...
    # until we get back to 1/n (i.e., remainder becomes 1)
    arr = []
    rem = 1
    
    while True:
        rem *= 2
        arr.append(rem // n)  # integer part of current fraction
        rem = rem % n         # remainder
        if rem == 1:
            break
    
    k = len(arr)  # period length
    
    # Calculate expected number of coin tosses
    ans = 0
    for i in range(k):
        if arr[i] == 1:
            ans += (2 ** (k - 1 - i)) * (i + 1)
    
    ans = ans * n + k
    
    # Reduce the fraction
    A = ans
    B = 2**k - 1
    G = gcd(A, B)
    A //= G
    B //= G
    
    # Add the pre-computed tosses for powers of 2
    print_fraction(A + B * pre, B)

solve()
