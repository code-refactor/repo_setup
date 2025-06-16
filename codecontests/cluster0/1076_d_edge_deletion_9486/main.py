#!/usr/bin/env python3

from library import fast_input, weighted_adj_list, dijkstra

input = fast_input()
n, m, k = map(int, input().split())

if k == 0:
    print(0)
    exit()

edges = []
edge_map = {}
for i in range(m):
    x, y, w = map(int, input().split())
    x, y = x-1, y-1
    edges.append((x, y, w))
    edge_map[(x, y)] = i
    edge_map[(y, x)] = i

graph = weighted_adj_list(n, edges)
dist, prev = dijkstra(graph, 0)

# Build shortest path tree
tree = [[] for _ in range(n)]
for i, p in enumerate(prev):
    if p != -1:
        tree[p].append(i)

# DFS to collect edges in order
result = []
stack = [0]
while stack and len(result) < k:
    v = stack.pop()
    for u in tree[v]:
        result.append(edge_map[(v, u)] + 1)
        if len(result) == k:
            break
        stack.append(u)

print(len(result))
if result:
    print(*result)
