#!/usr/bin/env python3
import math
from sys import stdin
from library import find_divisors, is_power_of_two_minus_one

q = int(input())
l = stdin.read().splitlines()

for i in l:
    n = int(i)
    
    # Check if n is one less than a power of 2 (i.e., 2^k - 1)
    # If not, then the optimal answer is (2^(k+1) - 1)
    # where k is the largest integer such that 2^k ≤ n
    if not is_power_of_two_minus_one(n):
        k = int(math.log2(n))
        print((1 << (k + 1)) - 1)
        continue
    
    # If n is of the form 2^k - 1, we need to find the largest divisor
    divisors = find_divisors(n)
    if len(divisors) > 2:  # If n has divisors other than 1 and itself
        # The largest proper divisor is the second largest divisor
        print(divisors[-2])
    else:
        # If n is prime, the answer is 1
        print(1)