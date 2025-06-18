#!/usr/bin/env python3

from library import read_str, init_dp_2d

s = read_str()
p = read_str()
n, m = len(s) + 1, len(p)
d = init_dp_2d(n, n, 0)

for x in range(1, n):
    i, j = x, m
    while i and j:
        j -= s[i - 1] == p[j - 1]
        i -= 1
    if not j:
        for y in range(i + 1): 
            d[x][y + x - i - m] = d[i][y] + 1
    for y in range(x): 
        d[x][y] = max(d[x][y], d[x - 1][y])

print(*d[-1])