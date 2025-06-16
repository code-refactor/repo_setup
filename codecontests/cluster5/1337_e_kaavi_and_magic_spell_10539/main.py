#!/usr/bin/env python3

from library import create_2d_table, MOD2

s = input().strip()
t = input().strip()

r_lim = len(t)
n = len(s)
dp = create_2d_table(n + 1, n + 1, 0)

for length in range(1, n + 1):
    for l in range(n + 1):
        r = l + length
        if r > n:
            break
        if length == 1:
            dp[l][r] = 2 if l >= r_lim or s[0] == t[l] else 0
            continue

        if l >= r_lim or s[length - 1] == t[l]:
            dp[l][r] += dp[l + 1][r]
            dp[l][r] %= MOD2
        if r - 1 >= r_lim or s[length - 1] == t[r - 1]:
            dp[l][r] += dp[l][r - 1]
            dp[l][r] %= MOD2

print(sum(dp[0][i] for i in range(r_lim, n + 1)) % MOD2)