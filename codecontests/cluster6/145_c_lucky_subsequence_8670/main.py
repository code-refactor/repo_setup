#!/usr/bin/env python3

from library import Combinatorics, MOD

def solve():
    n, k = map(int, input().split())
    a = [4, 7]
    d = {}
    idx = 0
    for p in range(1, 10):
        for m in range(1 << p):
            v = 0
            for i in range(p):
                v = v * 10 + a[(m >> i) & 1]
            d[v] = idx
            idx += 1
    
    c = [0] * idx
    b = 0
    for v in map(int, input().split()):
        if v in d:
            c[d[v]] += 1
        else:
            b += 1
    
    dp = [[0] * (idx + 1) for _ in range(idx + 1)]
    dp[0][0] = 1
    for m in range(1, idx + 1):
        dp[m][0] = dp[m - 1][0]
        cc = c[m - 1]
        for p in range(1, idx + 1):
            dp[m][p] = (dp[m - 1][p] + dp[m - 1][p - 1] * cc) % MOD
    
    res = 0
    d = dp[idx]
    comb = Combinatorics(max(idx, n) + 2)
    
    for p in range(max(0, k - b), min(idx, k) + 1):
        res = (res + d[p] * comb.fact[b] * comb.inv_fact[k - p] * comb.inv_fact[b - k + p]) % MOD
    print(res)

solve()
