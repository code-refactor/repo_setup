#!/usr/bin/env python3

from library import ints, adj_list

n, m = ints()
cats = list(ints())

edges = []
for _ in range(n-1):
    x, y = ints()
    edges.append((x-1, y-1))

graph = adj_list(n, edges)

visited = [False] * n
result = 0
queue = [(0, 0)]  # (node, consecutive_cats)
i = 0

while i < len(queue):
    node, consecutive = queue[i]
    visited[node] = True
    
    if cats[node]:
        consecutive += 1
    else:
        consecutive = 0
    
    if consecutive <= m:
        is_leaf = True
        for neighbor in graph[node]:
            if not visited[neighbor]:
                is_leaf = False
                queue.append((neighbor, consecutive))
        
        if is_leaf:
            result += 1
    
    i += 1

print(result)
