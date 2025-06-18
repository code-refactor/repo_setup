#!/usr/bin/env python3

def prime_factor(n):
    ass = []
    for i in range(2,int(n**0.5)+1):
        while n % i==0:
            ass.append(i)
            n = n//i
    if n != 1:
        ass.append(n)
    return ass

n = int(input())
p = list(set(prime_factor(n)))

if len(p) == 1:
    print(p[0])
else:
    print(1)