#!/usr/bin/env python3

import sys
sys.path.append('/home/justinchiu_cohere_com/minicode/codecontests/cluster3')
from library import Utils, TreeBuilder
from collections import deque

input = Utils.fast_io()
n = int(input())
l = list(map(int, input().split()))

# Read edges with weights
edges = []
for i in range(n-1):
    a, b, c = map(int, input().split())
    edges.append((a, b, c))

# Build adjacency list using library function
adj = TreeBuilder.from_edges(n, edges, indexed=1, weighted=True)

# Create edge weight lookup dictionary
d = {}
for a, b, c in edges:
    d[(a, b)] = c
    d[(b, a)] = c
# Convert to 0-indexed adjacency list for easier processing
graph = {i: set() for i in range(1, n+1)}
for a, b, c in edges:
    graph[a].add(b)
    graph[b].add(a)

z = [[0] for i in range(n+1)]
stack = deque()

# Find leaves
for i in graph:
    if len(graph[i]) == 1:
        stack.append([i, 0])

m = 0
while stack:
    x, y = stack.popleft()
    if len(graph[x]) >= 1:
        for i in graph[x]:
            t = i
            break
        q = d[(x, t)]  # Use direct lookup since we stored both directions
        z[t].append(y + l[x-1] - q)
        graph[t].remove(x)
        if len(graph[t]) == 1:
            stack.append([t, max(z[t])])

for i in range(1, n+1):
    z[i].sort()
    if len(z[i]) >= 3:
        m = max(m, l[i-1] + z[i][-2] + z[i][-1])
    m = max(m, z[i][-1] + l[i-1])

print(m)