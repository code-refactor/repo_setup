#!/usr/bin/env python3

n, t = map(int, input().split())

dp = [[[0] * 5 for _ in range(2 * t + 1)] for _ in range(n)]
dp[0][0] = [0, 1, 1, 1, 1]

for i in range(n - 1):
    for j in range(min(2 * t, i + 1)):
        if j % 2 == 0:
            for k in range(1, 4):
                for l in range(k + 1, 5):
                    dp[i + 1][j][l] += dp[i][j][k]
                    dp[i + 1][j + 1][l] += dp[i][j][k]
        else:
            for k in range(4, 1, -1):
                for l in range(k - 1, 0, -1):
                    dp[i + 1][j][l] += dp[i][j][k]
                    dp[i + 1][j + 1][l] += dp[i][j][k]

print(sum(dp[-1][2 * t]))
