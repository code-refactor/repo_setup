#!/usr/bin/env python3

from library import read_ints, read_str, init_dp_1d

n, m, k = read_ints()
s = read_str()
t = read_str()

n += 1
m += 1

p = [i for i in range(n * m - n) if (i + 1) % n]
r = p[::-1]

d = init_dp_1d(n * m, 0)

for i in p:
    if s[i % n] == t[i // n]: 
        d[i] = d[i - n - 1] + 1

f = d[:]

for y in range(k - 1):
    for i in p: 
        f[i] = max(f[i], f[i - 1], f[i - n])
    for i in r: 
        f[i] = f[i - d[i] * (n + 1)] + d[i]

print(max(f))