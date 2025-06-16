#!/usr/bin/env python3

from math import inf

def solve(s,t):
    if len(t) == 1:
        return 'YES' if t[0] in s else 'NO'
    for i in range(1,len(t)):
        dp = [[-inf]*(i+1) for _ in range(len(s)+1)]
        dp[0][0] = 0
        for j in range(len(s)):
            dp[j+1] = dp[j][:]
            for k in range(i+1):
                if k != i and s[j] == t[k]:
                    dp[j+1][k+1] = max(dp[j+1][k+1],dp[j][k])
                if dp[j][k]+i != len(t) and dp[j][k] != -inf and s[j] == t[dp[j][k]+i]:
                    dp[j+1][k] = max(dp[j+1][k],dp[j][k]+1)
        if any(dp[l][-1] == len(t)-i for l in range(len(s)+1)):
            return 'YES'
    return 'NO'

for _ in range(int(input())):
    s = input().strip()
    t = input().strip()
    print(solve(s,t))