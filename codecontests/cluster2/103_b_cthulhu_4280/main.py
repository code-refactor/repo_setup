#!/usr/bin/env python3

from library import read_ints, dfs_iterative, yes_no

n, m = read_ints()

# Cthulhu is a graph with exactly one cycle that contains all vertices
# This means the number of vertices must equal the number of edges
# And the graph must be connected
if n >= 3 and n == m:
    adj = [[] for _ in range(n + 1)]
    
    for _ in range(m):
        x, y = read_ints()
        adj[x].append(y)
        adj[y].append(x)

    # Check if the graph is connected
    visited = [False] * (n + 1)
    dfs_iterative(adj, 1, visited)
    
    # Check if all vertices are reachable from vertex 1
    is_connected = sum(1 for i in range(1, n+1) if visited[i]) == n
    
    print(yes_no(is_connected, "FHTAGN!", "NO"))
else:
    print("NO")