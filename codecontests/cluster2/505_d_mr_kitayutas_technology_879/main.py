#!/usr/bin/env python3

from library import read_ints, DSU

def solve():
    n, m = read_ints()
    n += 1  # Include 0-indexed extra node
    
    dsu = DSU(n)
    in_degree = [0] * n
    adj = [[] for _ in range(n)]
    
    # Build graph and DSU
    for _ in range(m):
        a, b = read_ints()
        adj[a].append(b)
        in_degree[b] += 1
        dsu.union(a, b)  # Connect nodes in DSU
    
    # Topological sort to detect cycles
    queue = [node for node in range(n) if in_degree[node] == 0]
    processed = 0
    
    while queue:
        node = queue.pop()
        processed += 1
        
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Mark components that have cycles as invalid
    valid_component = [True] * n
    for node in range(n):
        if in_degree[node] > 0:  # Part of a cycle
            root = dsu.find(node)
            valid_component[root] = False
    
    # Count valid components
    valid_count = 0
    for node in range(n):
        if dsu.find(node) == node and valid_component[node]:
            valid_count += 1
    
    print(n - valid_count)

solve()
