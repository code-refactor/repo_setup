#!/usr/bin/env python3

import sys
sys.setrecursionlimit(10**7)
input = sys.stdin.readline

INF = 10**9

n, m = [int(item) for item in input().split()]
s = input().rstrip()

count = [[0] * m for _ in range(m)]
ord_a = ord("a")
for c1, c2 in zip(s, s[1:]):
    c1 = ord(c1) - ord_a
    c2 = ord(c2) - ord_a
    if c1 != c2:
        count[c1][c2] += 1

sum_of_subset = [[0] * (1 << m) for _ in range(m)]
for i in range(m):
    for j in range(1 << m):
        if j == 0:
            continue
        lsb = j & -j
        sum_of_subset[i][j] = sum_of_subset[i][j ^ lsb] + count[i][lsb.bit_length() - 1]

adj_in_subset = [0] * (1 << m)
for i in range(1 << m):
    for j in range(m):
        if i & (1 << j):
            adj_in_subset[i] += sum_of_subset[j][i]

total_adj = adj_in_subset[-1]
dp = [INF] * (1 << m)
dp[0] = 0

for i in range(1 << m):
    for j in range(m):
        if i & 1 << j:
            continue
        cost = total_adj - adj_in_subset[i] - adj_in_subset[~i]
        dp[i | (1 << j)] = min(dp[i | (1 << j)], dp[i] + cost)
print(dp[-1])