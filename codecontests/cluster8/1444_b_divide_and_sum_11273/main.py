#!/usr/bin/env python3

n=int(input())
a=list(map(int,input().split()))
mod=998244353
def ncr(n, r, p):
    # initialize numerator
    # and denominator
    num = den = 1
    for i in range(r):
        num = (num * (n - i)) % p
        den = (den * (i + 1)) % p
    return (num * pow(den,
                      p - 2, p)) % p
a.sort()
print((ncr(2*n,n,mod)*(sum(a[n:])-sum(a[0:n])))%mod)