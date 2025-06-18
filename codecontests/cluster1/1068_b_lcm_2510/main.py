#!/usr/bin/env python3
from library import find_divisors

b = int(input())

# The solution here is to realize that lcm(a,b)/a = b/gcd(a,b)
# So we need to find the number of distinct values of b/gcd(a,b) where 1 <= a <= 10^18
# This is equivalent to finding the number of divisors of b

divisors = find_divisors(b)
print(len(divisors))