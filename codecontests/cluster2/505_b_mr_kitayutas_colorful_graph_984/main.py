#!/usr/bin/env python3

from library import read_ints, read_int, Graph

def solve():
    n, m = read_ints()
    
    # Store graphs by color
    graphs_by_color = {}
    
    for _ in range(m):
        u, v, c = read_ints()
        if c not in graphs_by_color:
            graphs_by_color[c] = Graph(n+1, directed=False)
        graphs_by_color[c].add_edge(u, v)
    
    q = read_int()
    for _ in range(q):
        u, v = read_ints()
        
        # Count how many colors can connect u and v
        paths = 0
        for color, graph in graphs_by_color.items():
            # Check if u and v are in the same component for this color
            visited_from_v = graph.dfs(v)
            if u in visited_from_v:
                paths += 1
        
        print(paths)

solve()