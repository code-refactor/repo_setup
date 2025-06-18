#!/usr/bin/env python3

from library import read_int, read_str, init_dp_1d

n = read_int()
s = read_str()
m = read_int()

a = init_dp_1d(n + 2, 0)
b = init_dp_1d(n + 2, 0)
q = init_dp_1d(n + 1, 0)
dp = [(0, 0)] * (n + 2)

for i in range(0, n):
    b[i] = b[i - 2] + (s[i] == 'b')
    a[i] = a[i - 2] + (s[i] == 'a')
    q[i] = q[i - 1] + (s[i] == '?')
  
for i in range(n - m, -1, -1):
    dp[i] = dp[i + 1]
    i_b = 1 if m % 2 == 1 else 2
    i_a = 1 if m % 2 == 0 else 2
  
    if not (b[i + m - i_b] - b[i - 2] or a[i + m - i_a] - a[i - 1]):
        t, r = dp[i + m]
        dp[i] = min((t - 1, r + q[i + m - 1] - q[i - 1]), dp[i])

print(dp[0][1])