#!/usr/bin/env python3

import sys
input = sys.stdin.readline
sys.setrecursionlimit(10 ** 5)

s = input()[:-1]
t = input()[:-1]

MOD = 998244353
r_lim = len(t)
n = len(s)
dp = [[0] * (n + 1) for i in range(n + 1)]


for length in range(1, n + 1):
    for l in range(n + 1):
        r = l + length
        if r > n:
            break
        if length == 1:
            if l >= r_lim or s[0] == t[l]:
                dp[l][r] = 2
            else:
                dp[l][r] = 0
            continue

        if l >= r_lim or s[length - 1] == t[l]:
            dp[l][r] += dp[l + 1][r]
            dp[l][r] %= MOD
        if r - 1 >= r_lim or s[length - 1] == t[r - 1]:
            dp[l][r] += dp[l][r - 1]
            dp[l][r] %= MOD


ans = 0
for i in range(r_lim, n + 1):
    ans += dp[0][i]
    ans %= MOD

print(ans)