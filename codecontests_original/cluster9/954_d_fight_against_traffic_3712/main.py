#!/usr/bin/env python3

from collections import deque
def bfs(s, graph):
    q = deque()
    d = [0] * len(graph)
    used = [False] * len(graph)
    used[s] = True
    q.append(s)
    while len(q):
        cur = q[0]
        q.popleft()
        for to in graph[cur]:
            if not used[to]:
                used[to] = True
                d[to] = d[cur] + 1
                q.append(to)
    return d
n, m, s, t = map(int, input().split())
graph = [set() for _ in range(n + 1)]
for i in range(m):
    u, v = map(int, input().split())
    graph[u].add(v)
    graph[v].add(u)
ds = bfs(s, graph)
dt = bfs(t, graph)
ans = 0
for u in range(1, n + 1):
    for v in range(u + 1, n + 1):
        if v not in graph[u] and min(ds[u] + dt[v], dt[u] + ds[v]) + 1 >= ds[t]:
            ans += 1
print(ans)
