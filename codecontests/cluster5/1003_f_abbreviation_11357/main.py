#!/usr/bin/env python3

from library import create_2d_table

n = int(input())
s = input()
allsum = len(s)
s = s.split()
eq = create_2d_table(n, n, False)
dp = create_2d_table(n, n)
for i in range(n):
    eq[i][i] = True
    for j in range(i):
        eq[i][j] = eq[j][i] = s[i] == s[j]
for i in range(n - 1, -1, -1):
    for j in range(n - 1, -1, -1):
        if eq[i][j]:
            if i < n - 1 and j < n - 1:
                dp[i][j] = dp[i + 1][j + 1] + 1
            else:
                dp[i][j] = 1
ans = allsum
for i in range(n):
    su = 0
    for j in range(1, n - i + 1):
        su += len(s[i + j - 1])
        cnt = 1
        pos = i + j
        while pos < n:
            if dp[i][pos] >= j:
                cnt += 1
                pos += j - 1
            pos += 1
        cur = allsum - su * cnt + cnt
        if cnt > 1 and ans > cur:
            ans = cur
print(ans)
