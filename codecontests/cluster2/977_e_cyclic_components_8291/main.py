#!/usr/bin/env python3

from library import read_ints, count_cyclic_components

n, m = read_ints()
adj = [[] for _ in range(n)]

for _ in range(m):
    u, v = read_ints()
    adj[u-1].append(v-1)
    adj[v-1].append(u-1)

print(count_cyclic_components(adj))