#!/usr/bin/env python3

n, m = map(int, input().split())
g = []
for i in range(n):
    g.append([])
for i in range(m):
    u, v = map(int, input().split())
    u-=1
    v-=1
    g[u]+=[v]
    g[v]+=[u]

start = max(range(n), key=lambda i: len(g[i]))
edges = []
vis = [False] * n
q = [start]
vis[start] = True
while q:
    u = q.pop(0)
    for v in g[u]:
        if vis[v]:
            continue
        vis[v] = True
        edges.append((u, v))
        q.append(v)

for u, v in edges:
    print(u+1, v+1)