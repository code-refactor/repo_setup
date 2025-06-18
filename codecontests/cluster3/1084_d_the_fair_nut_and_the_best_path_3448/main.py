#!/usr/bin/env python3

from library import setup_io, read_int, read_ints
from collections import deque

input = setup_io()

n = read_int()
l = read_ints()
graph = {i: set() for i in range(1, n+1)}
d = {}

# Read edges
for i in range(n-1):
    a, b, c = map(int, input().split())
    graph[a].add(b)
    graph[b].add(a)
    d[(a, b)] = c

# Initialize data structures
stack = deque()
z = [[0] for i in range(n+1)]

# Find leaf nodes to start
for i in graph:
    if len(graph[i]) == 1:
        stack.append([i, 0])

m = 0
while stack:
    x, y = stack.popleft()
    if len(graph[x]) >= 1:
        # Get the next node
        for i in graph[x]:
            t = i
            break
        
        # Get edge weight
        if (t, x) in d:
            q = d[(t, x)]
        else:
            q = d[(x, t)]
        
        # Update values
        z[t].append(y + l[x-1] - q)
        graph[t].remove(x)
        
        # Add next node to queue if it's now a leaf
        if len(graph[t]) == 1:
            stack.append([t, max(z[t])])

# Calculate result
for i in range(1, n+1):
    z[i].sort()
    if len(z[i]) >= 3:
        m = max(m, l[i-1] + z[i][-2] + z[i][-1])
    m = max(m, z[i][-1] + l[i-1])

print(m)