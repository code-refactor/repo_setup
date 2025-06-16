#!/usr/bin/env python3

from library import read_int, read_ints, DSU

n = read_int()
points = []
for _ in range(n):
    x, y = read_ints()
    points.append((x, y))

dsu = DSU(n)
for i in range(n):
    for j in range(i + 1, n):
        if points[i][0] == points[j][0] or points[i][1] == points[j][1]:
            dsu.union(i, j)

print(dsu.component_count() - 1)