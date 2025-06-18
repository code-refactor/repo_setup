#!/usr/bin/env python3

import sys
input = sys.stdin.readline

n = int(input())
mod = 10 ** 9 + 7
F = [0] * (n + 1)
F[0] = 1
for i in range(1, n + 1):
    F[i] = i * F[i - 1] % mod
iF = [0] * (n + 1)
iF[-1] = pow(F[-1], mod - 2, mod)
for i in range(n - 1, -1, -1):
    iF[i] = iF[i + 1] * (i + 1) % mod

def C(n, k):
    if k > n: return 0
    return F[n] * iF[n - k] * iF[k] % mod

ans = 0
for x in range((n + 1) // 2, n + 1):
    if x % 2: continue
    if x < n: cur = (C(x, n - x) + C(x - 1, n - x - 1)) % mod
    else: cur = 1
    cur = (cur * 2 * F[x]) % mod
    ans = (ans + cur) % mod
print(ans)