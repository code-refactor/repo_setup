#!/usr/bin/env python3

MOD = 998244353


def add(x, y):
    x += y
    while(x >= MOD):
        x -= MOD
    while(x < 0):
        x += MOD
    return x


def mul(x, y):
    return (x * y) % MOD


def binpow(x, y):
    z = 1
    while(y):
        if(y & 1):
            z = mul(z, x)
        x = mul(x, x)
        y >>= 1
    return z


def inv(x):
    return binpow(x, MOD - 2)


def divide(x, y):
    return mul(x, inv(y))


fact = []
N = 200000


def precalc():
    fact.append(1)
    for i in range(N):
        fact.append(mul(fact[i], i + 1))


def C(n, k):
    return divide(fact[n], mul(fact[k], fact[n - k]))


precalc()

NM = input()
[N, M] = NM.split()
N = int(N)
M = int(M)

res = 0

if (N > 2):
    res = mul(C(M, N - 1), mul(N - 2, binpow(2, N - 3)))


print(res)
