#!/usr/bin/env python3

from library import read_ints, read_str, init_dp_2d

n, k = read_ints()
s = read_str()
dp = init_dp_2d(n + 1, 26)
dp[0][0] = 1

for ch in s:
    j = ord(ch) - ord('a')
    for i in range(n, 0, -1):
        dp[i][j] = sum(dp[i - 1])

x = 0
y = 0
for i in range(n, -1, -1):
    if x + sum(dp[i]) >= k:
        print(k * n - y - (k - x) * i)
        break
    x += sum(dp[i])
    y += i * sum(dp[i])
else:
    print(-1)