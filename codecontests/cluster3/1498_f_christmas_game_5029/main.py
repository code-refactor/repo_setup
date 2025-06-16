#!/usr/bin/env python3

from library import TreeBuilder, Utils
from collections import deque

input = Utils.fast_io()

n, k = map(int, input().split())
edges = Utils.read_tree_edges(n, indexed=1, weighted=False)
adj = TreeBuilder.from_edges(n, edges, indexed=1, weighted=False)
a = list(map(int, input().split()))

#bfs
p = [i for i in range(n)]
vlis = []
q = deque([0])
while q:
    v = q.popleft()
    vlis.append(v)

    for nex in adj[v]:
        if nex != p[v]:
            p[nex] = v
            q.append(nex)

#dp-first
dp = [[0] * (2*k) for i in range(n)]
for ind in range(n-1,-1,-1):
    v = vlis[ind]
    dp[v][0] ^= a[v]

    for nex in adj[v]:
        if nex != p[v]:
            for nk in range(2*k):
                dp[v][(nk+1) % (2*k)] ^= dp[nex][nk]

#dp2
ans = [None] * n
for v in vlis:
    if v == 0:
        now = 0
        for i in range(k, 2*k):
            now ^= dp[v][i]
        ans[v] = min(now, 1)
    else:
        pcopy = [dp[p[v]][i] for i in range(2*k)]
        for i in range(2*k):
            pcopy[(i+1) % (2*k)] ^= dp[v][i]
        for i in range(2*k):
            dp[v][(i+1) % (2*k)] ^= pcopy[i]

        now = 0
        for i in range(k, 2*k):
            now ^= dp[v][i]
        ans[v] = min(now, 1)

print(*ans)