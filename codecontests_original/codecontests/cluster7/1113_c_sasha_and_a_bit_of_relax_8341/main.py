#!/usr/bin/env python3

n = int(input())
a = [int(x) for x in input().split()]

pref = [0]
for i in range(n):
    pref.append(pref[-1] ^ a[i])

dp = [[0 for i in range(2**20 + 5)] for j in range(2)]
ans = 0
for i in range(len(pref)):
    ans += dp[i % 2][pref[i]]
    dp[i % 2][pref[i]] += 1
    #print(ans, pref[i])
print(ans)
