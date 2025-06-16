#!/usr/bin/env python3

from library import tree_depth_bfs

n = int(input())
a = [[] for _ in range(n)]
roots = []

for i in range(n):
    x = int(input())
    if x > 0:
        a[x-1].append(i)
    else:
        roots.append(i)

print(max([tree_depth_bfs(a, root) for root in roots]))
    
