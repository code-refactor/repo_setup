#!/usr/bin/env python3

mod = 1000000007

#gcd(a, m) = 1
def inv_mod(a, m):
    a %= m
    return pow(a, m-2, m)


a = input()
k = int(input())
t = len(a)
d = 0
for i, c in enumerate(a):
    if not int(c) % 5:
        d += pow(2, i, mod)
        d %= mod
print(d*(pow(2, (k*t)%(mod-1), mod)-1)*inv_mod(pow(2, t, mod)-1, mod)%mod)
