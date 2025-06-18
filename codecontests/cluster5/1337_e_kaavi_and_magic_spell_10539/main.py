#!/usr/bin/env python3

from library import read_str, init_dp_2d, MOD

s = read_str()
t = read_str()

r_lim = len(t)
n = len(s)
dp = init_dp_2d(n + 1, n + 1)

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