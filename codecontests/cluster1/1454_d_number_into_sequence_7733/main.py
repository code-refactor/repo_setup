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

tc = int(input())
for i in range(tc):
    integer = int(input())
    factors = prime_factorize(integer)
    
    if not factors:
        print(f'1\n{integer}')
    else:
        # Count frequencies
        from collections import Counter
        factor_counts = Counter(factors)
        # Sort by count in descending order
        sorted_factors = sorted(factor_counts.items(), key=lambda x: x[1], reverse=True)
        
        banyak, count = sorted_factors[0][0], sorted_factors[0][1]
        last = integer // (banyak**(count-1))
        print(count)
        print(f'{banyak} '*(count-1), end='')
        print(last)
