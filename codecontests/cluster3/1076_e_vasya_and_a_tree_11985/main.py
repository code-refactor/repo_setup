#!/usr/bin/env python3

from library import setup_io, read_int, read_int_tuple, bootstrap
from collections import defaultdict

input = setup_io()

@bootstrap
def dfs(u, i, p):
    global d, s
    s += -d[i-1]

    for j in val[u]:
        d[i+j[0]] += j[1]
        s += j[1]

    ans[u] = s
    for j in adj[u]:
        if j != p:
            yield dfs(j, i+1, u)
    for j in val[u]:
        d[i + j[0]] += -j[1]
        s += -j[1]
    s += d[i-1]

    yield

# Read tree
n = read_int()
adj = [[] for i in range(n+1)]
for j in range(n-1):
    u, v = read_int_tuple()
    adj[u].append(v)
    adj[v].append(u)

# Read queries
val = [[] for i in range(n+1)]
m = read_int()
for j in range(m):
    v, d, va = read_int_tuple()
    val[v].append([d, va])

# Process the tree with DFS
s = 0
d = defaultdict(lambda: 0)
ans = [0 for i in range(n+1)]
dfs(1, 0, 0)
print(*ans[1:])