#!/usr/bin/env python3

import sys

MOD = int(1e9) + 9

def inv(n):
    return pow(n, MOD - 2, MOD)

def combo(n):
    rv = [0 for __ in range(n + 1)]
    rv[0] = 1
    for k in range(n):
        rv[k + 1] = rv[k] * (n - k) %  MOD * inv(k + 1) % MOD
    return rv

with sys.stdin as fin, sys.stdout as fout:
    n, w, b = map(int, next(fin).split())

    combw = combo(w - 1)
    combb = combo(b - 1)

    ans = 0
    for black in range(max(1, n - w), min(n - 2, b) + 1):
        ans = (ans + (n - 1 - black) * combw[n - black - 1] % MOD * combb[black - 1]) % MOD

    for f in w, b:
        for k in range(1, f + 1):
            ans = k * ans % MOD

    print(ans, file=fout)
