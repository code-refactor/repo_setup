#!/usr/bin/env python3

from library import Combinatorics

MAX_N = 55
comb = Combinatorics(MAX_N, use_mod=False)

studc, roomc = map(int, input().split())
arr = list(map(int, input().split()))

upto = [0] * MAX_N
for i in range(1, MAX_N):
    dp = [[0] * MAX_N for _ in range(MAX_N)]
    dp[0][0] = 1
    for j in range(roomc):
        for k in range(0, min(studc, i * arr[j]) + 1):
            for l in range(0, studc - k + 1):
                dp[j + 1][k + l] += dp[j][l] * comb.C(studc - l, k)
    
    upto[i] = dp[roomc][studc]
    
ans = 0
for i in range(1, MAX_N):
    ans += (upto[i] - upto[i - 1]) * i

print('%.15f' % (ans / (roomc ** studc)))
