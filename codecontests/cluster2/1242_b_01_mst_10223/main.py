#!/usr/bin/env python3

from library import read_ints, DSU

def solve():
    n, m = read_ints()
    
    # If no weight-1 edges, all weight-0 edges -> MST weight = 0
    if m == 0:
        print(0)
        return
    
    # Build adjacency sets for faster lookup of weight-1 edges
    weight1_edges = set()
    for _ in range(m):
        x, y = read_ints()
        weight1_edges.add((min(x,y), max(x,y)))
    
    # Use BFS/DFS to find components connected by weight-0 edges
    visited = [False] * (n+1)
    components = 0
    
    def dfs(start):
        stack = [start]
        while stack:
            v = stack.pop()
            if visited[v]:
                continue
            visited[v] = True
            # Connect to all nodes not connected by weight-1 edge
            for u in range(1, n+1):
                if not visited[u] and (min(v,u), max(v,u)) not in weight1_edges:
                    stack.append(u)
    
    # Count connected components in complement graph (weight-0 edges)
    for i in range(1, n+1):
        if not visited[i]:
            dfs(i)
            components += 1
    
    # MST weight = number of components - 1 (need weight-1 edges to connect)
    print(components - 1)

solve()