#!/usr/bin/env python3

import sys, io, os
input = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline
read = lambda: map(int, input().split())
from heapq import heappush, heappop

inf = 1e10
n, m = read()
e = {}
for _ in range(m):
    v, u, w = read()
    v -= 1
    u -= 1
    if v not in e:
        e[v] = []
    if u not in e:
        e[u] = []
    e[v].append((u, w))
    e[u].append((v, w))
d = [inf] * n
d[0] = 0
q = []
td = [0] * n
heappush(q, (0, 0))
while q:
    vd, v = heappop(q)
    l = []
    for u, w in e[v]:
        td[u] = w
        l.append(u)
    for u in l:
        tdu = td[u]
        for x, w in e[u]:
            cv = vd + (tdu + w) ** 2
            if cv < d[x]:
                d[x] = cv
                heappush(q, (cv, x))
for i in range(n):
    if d[i] == inf:
        d[i] = -1
print(' '.join(map(str, d)))