#!/usr/bin/env python3

from sys import stdin
from collections import deque


def bfs(x):
    vis[x] = True
    q = deque([x])
    ans = 1
    while q:
        cur = q.popleft()
        ans &= len(g[cur]) == 2
        for x in g[cur]:
            if not vis[x]:
                vis[x] = True
                q.append(x)
    return ans


n, m = map(int, stdin.readline().split())
g = [[] for _ in range(n)]
vis = [False]*n
ans = 0
for _ in range(m):
    u, v = map(lambda x: int(x) - 1, stdin.readline().split())
    g[u].append(v)
    g[v].append(u)

for x in range(n):
    if not vis[x]:
        ans += bfs(x)

print(ans)

  		 		 	   	 				 	     	   	