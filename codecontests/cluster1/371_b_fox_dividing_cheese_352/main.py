#!/usr/bin/env python3

def prime_factorize(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    if n > 2:
        factors.append(n)
    return factors

def take_input(s):          #for integer inputs
    if s == 1:  return int(input())
    return map(int, input().split())

def factor_count(factors, k):
    return factors.count(k)
        
a, b = take_input(2)
count = 0
if a == b:
    print(0)
    exit()

a_factors = prime_factorize(a)
b_factors = prime_factorize(b)

a_fac_2 = factor_count(a_factors, 2)
a_fac_3 = factor_count(a_factors, 3)
a_fac_5 = factor_count(a_factors, 5)

b_fac_2 = factor_count(b_factors, 2)
b_fac_3 = factor_count(b_factors, 3)
b_fac_5 = factor_count(b_factors, 5)

# Remove factors of 2, 3, 5 to get the remaining part
a_remaining = a
for _ in range(a_fac_2): a_remaining //= 2
for _ in range(a_fac_3): a_remaining //= 3
for _ in range(a_fac_5): a_remaining //= 5

b_remaining = b
for _ in range(b_fac_2): b_remaining //= 2
for _ in range(b_fac_3): b_remaining //= 3
for _ in range(b_fac_5): b_remaining //= 5

if a_remaining != b_remaining:
    print(-1)
else:
    print(abs(a_fac_2 - b_fac_2) + abs(a_fac_3 - b_fac_3) + abs(a_fac_5 - b_fac_5))
