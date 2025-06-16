#!/usr/bin/env python3

from library import create_3d_table, MOD2

x = input()
y = input()
x = [ord(ch) - 97 for ch in x]
y = [ord(ch) - 97 for ch in y]

m, n = len(x), len(y)

v1 = [1] * (m + 1)
v2 = [1] * (n + 1)
for i in range(m - 2, -1, -1):
    if x[i] != x[i + 1]:
        v1[i] += v1[i + 1]
for i in range(n - 2, -1, -1):
    if y[i] != y[i + 1]:
        v2[i] += v2[i + 1]

dp = create_3d_table(m + 1, n + 1, 27, 0)
for i in range(m - 1, -1, -1):
    for j in range(n - 1, -1, -1):
        for k in range(27):
            if x[i] == k:
                if y[j] != k:
                    dp[i][j][k] = (dp[i][j + 1][y[j]] + v1[i]) % MOD2
            elif y[j] == k:
                dp[i][j][k] = (dp[i + 1][j][x[i]] + v2[j]) % MOD2
            else:
                dp[i][j][k] = (dp[i + 1][j][x[i]] + dp[i][j + 1][y[j]] + (x[i] != y[j]) * (v2[j] + v1[i])) % MOD2

print(sum(dp[i][j][26] for i in range(m) for j in range(n)) % MOD2)