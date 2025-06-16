#!/usr/bin/env python3

f = lambda: list(map(int, input().split()))
d = lambda x, y: (x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2
r = lambda x, y, z: (x[0] - y[0]) * (x[1] - z[1]) == (x[1] - y[1]) * (x[0] - z[0])

n = int(input())
t = [f() for i in range(n)]

j = k = -1
b = c = 0

x = t.pop()
for i in range(n - 1):
    a = d(x, t[i])
    if j < 0 or a < b: j, b = i, a

y = t.pop(j)
for i in range(n - 2):
    if r(x, y, t[i]): continue
    a = d(x, t[i])
    if k < 0 or a < c: k, c = i, a

print(n, j + 1, k + 2 - (j > k))