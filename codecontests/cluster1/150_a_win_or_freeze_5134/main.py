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

n = int(input())
arr = prime_factorize(n)

if n==1 or len(arr)==1:
    print(1)
    print(0)
elif len(arr)==2:
    print(2)
else:
    x = arr[0]*arr[1]
    print(1)
    print(x)