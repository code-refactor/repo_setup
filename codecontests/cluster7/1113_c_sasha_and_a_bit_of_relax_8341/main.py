#!/usr/bin/env python3
from library import read_array, prefix_xor

n = int(input())
a = read_array(n)

pref = prefix_xor(a)

dp = [[0 for i in range(2**20 + 5)] for j in range(2)]
ans = 0
for i in range(len(pref)):
    ans += dp[i % 2][pref[i]]
    dp[i % 2][pref[i]] += 1
print(ans)
