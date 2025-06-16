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

t=int(input())
for i in range(t):
    n=int(input())
    if n==1:
        print(0)
    else:
        if n%3!=0:
            print(-1)
        else:
            factors = prime_factorize(n)
            threes = factors.count(3)
            twos = factors.count(2)
            # Check if there are any other prime factors
            if len(factors) != threes + twos or twos > threes:
                print(-1)
            else:
                print(2*threes-twos)
