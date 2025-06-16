#!/usr/bin/env python3

from library import ints

n, m = ints()
edges = []
for _ in range(m):
    a, b = ints()
    edges.append((a, b))

degree = [0] * (n+1)
for a, b in edges:
    degree[a] += 1
    degree[b] += 1

c1 = sum(1 for i in range(1, n+1) if degree[i] == 1)
c2 = sum(1 for i in range(1, n+1) if degree[i] == 2)
cs = sum(1 for i in range(1, n+1) if degree[i] == n-1)

if c1 == 2 and c2 == n-2:
    print("bus topology")
elif c2 == n:
    print("ring topology")
elif c1 == n-1 and cs == 1:
    print("star topology")
else:
    print("unknown topology")