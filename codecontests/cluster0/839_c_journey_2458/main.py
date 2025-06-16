#!/usr/bin/env python3

from library import ints, int_inp, adj_list
from collections import deque

n = int_inp()
edges = []
for _ in range(n-1):
    a, b = ints()
    edges.append((a-1, b-1))

graph = adj_list(n, edges)
visited = [False] * n
result = 0

queue = deque([(0, 0, 1)])  # (node, depth, probability)
while queue:
    v, d, r = queue.popleft()
    visited[v] = True
    
    unvisited_neighbors = [u for u in graph[v] if not visited[u]]
    for u in unvisited_neighbors:
        prob_factor = len(graph[v]) - (v != 0)
        queue.append((u, d+1, r * prob_factor))
    
    if v != 0 and len(graph[v]) == 1:
        result += d / r

print(result)