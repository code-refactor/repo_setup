#!/usr/bin/env python3

from library import read_ints, init_dp_3d

n1, n2, k1, k2 = read_ints()
k1 = min(k1, n1)
k2 = min(k2, n2)

dp = init_dp_3d(n1 + 1, n2 + 1, 2)

for i in range(k1 + 1):
    dp[i][0][0] = 1
for i in range(k2 + 1):
    dp[0][i][1] = 1

MOD = 100000000

for i in range(1, n1 + 1):
    for j in range(1, n2 + 1):
        dp[i][j][0] = sum(dp[k][j][1] for k in range(max(0, i - k1), i)) % MOD
        dp[i][j][1] = sum(dp[i][k][0] for k in range(max(0, j - k2), j)) % MOD

print(sum(dp[n1][n2]) % MOD)