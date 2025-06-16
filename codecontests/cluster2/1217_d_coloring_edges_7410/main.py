#!/usr/bin/env python3

from library import read_ints, Graph

def solve():
    n, m = read_ints()
    
    # Create directed graph and store edges
    graph = Graph(n+1, directed=True)
    edges = []
    edge_to_idx = {}
    
    for i in range(m):
        x1, x2 = read_ints()
        edges.append((x1, x2))
        edge_to_idx[(x1, x2)] = i
        graph.add_edge(x1, x2)
    
    # Use DFS to detect back edges (cycles)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * (n+1)
    edge_colors = [1] * m  # Default all edges to color 1
    has_cycle = False
    
    def dfs(u):
        nonlocal has_cycle
        color[u] = GRAY
        
        for v in graph.neighbors(u):
            if color[v] == GRAY:
                # Back edge found - this creates a cycle
                has_cycle = True
                edge_colors[edge_to_idx[(u, v)]] = 2  # Color back edge with 2
            elif color[v] == WHITE:
                dfs(v)
        
        color[u] = BLACK
    
    # Run DFS from all unvisited nodes
    for i in range(1, n+1):
        if color[i] == WHITE:
            dfs(i)
    
    if has_cycle:
        print(2)
    else:
        print(1)
    
    print(' '.join(map(str, edge_colors)))

solve()
