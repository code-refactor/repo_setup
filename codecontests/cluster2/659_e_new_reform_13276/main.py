#!/usr/bin/env python3

from library import read_ints, has_cycle

def main():
    n, m = read_ints()
    adj = [[] for _ in range(n+1)]
    
    for _ in range(m):
        x, y = read_ints()
        adj[x].append(y)
        adj[y].append(x)
    
    # Count the number of acyclic components
    visited = [False] * (n+1)
    acyclic_components = 0
    
    for i in range(1, n+1):
        if not visited[i]:
            # Check if this component has a cycle
            if not has_cycle(adj, i, visited):
                acyclic_components += 1
    
    print(acyclic_components)

if __name__ == "__main__":
    main()