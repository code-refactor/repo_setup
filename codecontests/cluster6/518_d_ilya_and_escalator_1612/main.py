#!/usr/bin/env python3

from library import FastIO

n, p, t = FastIO.read_string().split()
n = int(n)
p = float(p)
t = int(t)

def CC(nn,k):
    tmp = n
    t = max(nn - k, k)
    for i in range(1, min(nn - k, k) + 1):
        tmp = tmp * (t + i) * (1 - p) / i
    if k > nn - k:
        tmp = tmp * pow(1-p,k + k - nn)
    return tmp

def C(n, k):
    tmp = 1
    if n - k > k:
        tmp = tmp * pow(1 - p, n - k - k)
    else:
        tmp = tmp * pow(p, k + k - n)
    t = max(n - k, k)
    for i in range(1, min(n - k, k) + 1):
        tmp = tmp * (t + i) * p * (1 - p) / i

    return tmp


if n >= t:
    print(f"{t * p:.12f}")
elif p != 1 and p != 0:
    a = 0
    b = 0
    for i in range(n):
        q = C(t, i)
        a = a + q * i
        b = b + q
    a = a + (1 - b) * n
    print(f"{a:.12f}")
    b = n
    for i in range(t - n):
        b = b + CC(i + 1,n + i)
    b = b * pow(p,n)
    #print(a + b)
else:
    if p == 1:
        print(f"{n:.12f}")
    else:
        print(f"{0:.12f}")
