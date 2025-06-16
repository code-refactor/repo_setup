#!/usr/bin/env python3

import sys
sys.path.append('..')

n = int(input())
r = [[] for i in range(n + 1)]
r[1] = [0]
for i in range(n - 1):
    a, b = map(int, input().split())
    r[a].append(b)
    r[b].append(a)
t = list(map(int, input().split()))
u, v = [0] * (n + 1), [0] * (n + 1)
for i, j in enumerate(t, 1):
    if j < 0: u[i] = - j
    else: v[i] = j
# print(u,v)
t, p = [1], [0] * (n + 1)
while t:
    a = t.pop()
    for b in r[a]:
        if p[b]: continue
        p[b] = a
        t.append(b)
k = [len(t) for t in r]
t = [a for a in range(2, n + 1) if k[a] == 1]
x, y = [0] * (n + 1), [0] * (n + 1)
while t:
    a = t.pop()
    b = p[a]
    x[b] = max(x[b], u[a])
    y[b] = max(y[b], v[a])
    k[b] -= 1
    if k[b] == 1:
        t.append(b)
        if u[b] > 0:
            if x[b] - y[b] > u[b]:
                u[b], v[b] = x[b], x[b] - u[b]
            else: u[b], v[b] = y[b] + u[b], y[b]
        else:
            if y[b] - x[b] > v[b]:
                u[b], v[b] = y[b] - v[b], y[b]
            else: u[b], v[b] = x[b], x[b] + v[b]
print(u[1] + v[1])