#!/usr/bin/env python3

from library import read_ints, yes_no

def main():
    n, m = read_ints()
    
    # Cthulhu is a graph with exactly one cycle that contains all vertices
    # Build adjacency list
    adj = [[] for _ in range(n+1)]
    for _ in range(m):
        x, y = read_ints()
        adj[x].append(y)
        adj[y].append(x)
    
    # Perform DFS to check connectivity and count cycles
    visited = [False] * (n+1)
    parent = [0] * (n+1)
    cycles = 0
    
    def dfs(u):
        nonlocal cycles
        visited[u] = True
        
        for v in adj[u]:
            if not visited[v]:
                parent[v] = u
                dfs(v)
            elif v != parent[u]:
                # Found a back edge (part of a cycle)
                cycles += 1
    
    # Start DFS from vertex 1
    dfs(1)
    
    # Check if all vertices are visited (graph is connected)
    is_connected = all(visited[i] for i in range(1, n+1))
    
    # Each cycle is counted twice in an undirected graph
    # Cthulhu must have exactly one cycle
    is_cthulhu = is_connected and cycles/2 == 1
    
    print(yes_no(is_cthulhu, "FHTAGN!", "NO"))

if __name__ == "__main__":
    main()
