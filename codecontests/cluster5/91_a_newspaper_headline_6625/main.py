#!/usr/bin/env python3

import math
from library import read_str, init_dp_2d

a = read_str()
b = read_str()
na = len(a)
nb = len(b)

dp = init_dp_2d(na + 1, 26, -1)

for i in range(na - 1, -1, -1):
    for j in range(26):
        dp[i][j] = dp[i+1][j]
    dp[i][ord(a[i]) - 97] = i

cp = 0
ans = 1
i = 0

while i < nb:
    if cp == na:
        ans += 1
        cp = 0
    if dp[cp][ord(b[i]) - 97] == -1:
        ans += 1
        cp = 0
        if dp[cp][ord(b[i]) - 97] == -1:
            ans = math.inf
            break
    cp = dp[cp][ord(b[i]) - 97] + 1
    i += 1

print(ans if ans != math.inf else -1)