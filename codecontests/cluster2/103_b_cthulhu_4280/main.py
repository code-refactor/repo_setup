#!/usr/bin/env python3

from library import read_ints, Graph, print_yes_no_custom

n, m = read_ints()

if n >= 3 and n == m:
    graph = Graph(n + 1)
    for _ in range(m):
        u, v = read_ints()
        graph.add_edge(u, v)
    
    visited = graph.dfs(1)
    print_yes_no_custom(len(visited) == n, "FHTAGN!", "NO")
else:
    print("NO")