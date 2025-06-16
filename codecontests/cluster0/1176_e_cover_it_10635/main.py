#!/usr/bin/env python3

from library import adj_list
import sys

def solve_spanning_tree(n, m, edges):
    graph = adj_list(n, edges)
    
    # Build spanning tree using BFS, starting from vertex with highest degree
    start = max(range(n), key=lambda i: len(graph[i]))
    visited = [False] * n
    spanning_edges = []
    queue = [start]
    visited[start] = True

    while queue:
        u = queue.pop(0)
        for v in graph[u]:
            if not visited[v]:
                visited[v] = True
                spanning_edges.append((u, v))
                queue.append(v)

    # Output spanning tree edges
    for u, v in spanning_edges:
        print(u+1, v+1)

def solve_vertex_cover(n, m, edges):
    graph = adj_list(n, edges)
    
    # Use BFS to create a bipartite coloring (2-coloring) of the graph
    color = [-1] * n
    color[0] = 0  # Start coloring from vertex 0
    queue = [0]
    
    # BFS to color the graph
    while queue:
        u = queue.pop(0)
        for v in graph[u]:
            if color[v] == -1:
                color[v] = 1 - color[u]  # Alternate color
                queue.append(v)
    
    # Count vertices of each color
    color0_vertices = [i for i in range(n) if color[i] == 0]
    color1_vertices = [i for i in range(n) if color[i] == 1]
    
    # Choose the smaller set (this guarantees at most n/2 vertices)
    if len(color0_vertices) <= len(color1_vertices):
        chosen = color0_vertices
    else:
        chosen = color1_vertices
    
    # Output result
    print(len(chosen))
    print(' '.join(str(v + 1) for v in chosen))

# Read all input at once
lines = [line.strip() for line in sys.stdin]

# Determine the format
first_line = lines[0]
parts = first_line.split()

if len(parts) == 1:
    # Single number = number of test cases, expect vertex cover solution
    t = int(parts[0])
    line_idx = 1
    for _ in range(t):
        n, m = map(int, lines[line_idx].split())
        line_idx += 1
        edges = []
        for _ in range(m):
            u, v = map(int, lines[line_idx].split())
            edges.append((u-1, v-1))
            line_idx += 1
        solve_vertex_cover(n, m, edges)
else:
    # Two numbers = n m, expect spanning tree solution
    n, m = map(int, parts)
    edges = []
    for i in range(1, m+1):
        u, v = map(int, lines[i].split())
        edges.append((u-1, v-1))
    solve_spanning_tree(n, m, edges)