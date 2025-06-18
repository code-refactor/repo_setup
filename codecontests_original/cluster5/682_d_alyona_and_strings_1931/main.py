#!/usr/bin/env python3

n, m, k = map(int, input().split())
s, t = input(), input()

n += 1
m += 1

p = [i for i in range(n * m - n) if (i + 1) % n]
r = p[::-1]

d = [0] * n * m

for i in p:
    if s[i % n] == t[i // n]: d[i] = d[i - n - 1] + 1

f = d[:]

for y in range(k - 1):
    for i in p: f[i] = max(f[i], f[i - 1], f[i - n])
    for i in r: f[i] = f[i - d[i] * (n + 1)] + d[i]

print(max(f))