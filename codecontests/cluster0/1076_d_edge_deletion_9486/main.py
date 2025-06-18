#!/usr/bin/env python3

from library import parse_ints
import sys
import heapq

# Read input
n, m, k = parse_ints()

# Initialize graph and edge mapping
g = [[] for _ in range(n)]
toid = {}  # Map edge (u,v) to its original index

# Read edges and build graph
for i in range(m):
    x, y, w = parse_ints()
    x, y = x-1, y-1  # Convert to 0-indexed
    # Store edges as (weight, node) for the graph
    g[x].append((w, y))
    g[y].append((w, x))
    # Map both directions to the same edge ID
    toid[(x, y)] = i
    toid[(y, x)] = i

# Handle special case
if k == 0:
    print(0)
    sys.exit(0)

# Custom Dijkstra implementation to match expected output exactly
INF = 10**18
def dijkstra(s, edge):
    n = len(edge)
    dist = [INF] * n
    prev = [-1] * n
    dist[s] = 0
    edgelist = []
    heapq.heappush(edgelist, (dist[s], s))
    
    while edgelist:
        minedge = heapq.heappop(edgelist)
        if dist[minedge[1]] < minedge[0]:
            continue
        v = minedge[1]
        for e in edge[v]:
            if dist[e[1]] > dist[v] + e[0]:
                dist[e[1]] = dist[v] + e[0]
                prev[e[1]] = v
                heapq.heappush(edgelist, (dist[e[1]], e[1]))
    
    return dist, prev

# Run Dijkstra's algorithm from node 0
dist, prev = dijkstra(0, g)

# Build the shortest paths tree
G = [[] for i in range(n)]
for i, p in enumerate(prev):
    if prev[i] != -1:
        G[p].append(i)

# Use DFS to traverse the shortest paths tree
s = [0]  # Start from node 0
order = []
while s:
    v = s.pop()
    order.append(v)
    for u in G[v]:
        s.append(u)

# Select up to k edges from the shortest paths tree
ans = []
for v in order:
    for u in G[v]:
        # Add the edge to our answer (1-indexed)
        ans.append(toid[(v, u)] + 1)
        if len(ans) == k:
            break
    else:
        continue
    break

# Output the result
print(len(ans))
print(*ans)
