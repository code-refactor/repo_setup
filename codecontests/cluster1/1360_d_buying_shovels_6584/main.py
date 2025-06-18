#!/usr/bin/env python3
from library import find_divisors

def solve():
    n, k = map(int, input().split())
    
    # If k >= n, we can buy 1 package of n shovels
    if k >= n:
        return 1
    
    # Find all divisors of n
    divisors = find_divisors(n)
    
    # Find the largest divisor that is <= k
    # This will minimize the number of packages (n // divisor)
    best_divisor = 1
    for divisor in divisors:
        if divisor <= k:
            best_divisor = max(best_divisor, divisor)
    
    return n // best_divisor

def main():
    t = int(input())
    for _ in range(t):
        print(solve())

if __name__ == "__main__":
    main()