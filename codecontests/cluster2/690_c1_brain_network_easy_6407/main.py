#!/usr/bin/env python3

from library import read_ints, print_yes_no_custom

def solve():
    n, m = read_ints()
    # Special case: single node
    if n == 1:
        if m == 0:
            print_yes_no_custom(True, "yes", "no")
        else:
            print_yes_no_custom(False, "yes", "no")
        return
    
    # For a valid tree with n nodes: must have exactly n-1 edges
    if m != n - 1:
        print_yes_no_custom(False, "yes", "no")
        return
    
    # Read edges into adjacency list
    adj = [[] for _ in range(n+1)]
    for _ in range(m):
        u, v = read_ints()
        adj[u].append(v)
        adj[v].append(u)
    
    # Check connectivity and detect cycles using DFS
    visited = [False] * (n+1)
    has_cycle = False
    
    def dfs(node, parent):
        nonlocal has_cycle
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]:
                dfs(neighbor, node)
            elif neighbor != parent:
                # Back edge found - cycle detected
                has_cycle = True
    
    # Start DFS from node 1
    dfs(1, -1)
    
    # Check if all nodes are reachable
    for i in range(1, n+1):
        if not visited[i]:
            print_yes_no_custom(False, "yes", "no")
            return
    
    # Check if there's a cycle
    if has_cycle:
        print_yes_no_custom(False, "yes", "no")
        return
    
    # Connected, acyclic, and n-1 edges -> valid tree
    print_yes_no_custom(True, "yes", "no")

solve()
