#!/usr/bin/env python3

from library import DSU, read_int, read_ints

def solve_b():
    n = read_int()
    p = read_ints()
    dsu = DSU(n)
    for i, x in enumerate(p):
        dsu.union(i, x - 1)
    return [dsu.component_size(i) for i in range(n)]

t = read_int()
for _ in range(t):
    print(*solve_b())
