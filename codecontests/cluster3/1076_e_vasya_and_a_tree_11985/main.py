#!/usr/bin/env python3

from library import TreeBuilder, Utils
from collections import defaultdict

Utils.set_recursion_limit(10**5)

n = int(input())
edges = Utils.read_tree_edges(n, indexed=1, weighted=False)
adj = TreeBuilder.from_edges(n, edges, indexed=1, weighted=False)

val = [[] for _ in range(n)]
m = int(input())
for _ in range(m):
    v, d, va = map(int, input().split())
    val[v-1].append([d, va])

@Utils.bootstrap
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

s = 0
d = defaultdict(lambda: 0)
ans = [0] * n
dfs(0, 0, -1)
print(*ans)
