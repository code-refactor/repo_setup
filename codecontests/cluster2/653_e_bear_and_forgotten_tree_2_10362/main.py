#!/usr/bin/env python3

from library import read_ints, print_yes_no_custom

def solve():
    n, m, k = read_ints()
    
    # Build adjacency sets for forbidden edges
    forbidden = [set() for _ in range(n+1)]
    node1_blocked_degree = 0
    
    for _ in range(m):
        a, b = read_ints()
        forbidden[a].add(b)
        forbidden[b].add(a)
        if a == 1 or b == 1:
            node1_blocked_degree += 1
    
    # Check if node 1 can have degree k
    max_degree_possible = n - 1 - node1_blocked_degree
    if max_degree_possible < k:
        print_yes_no_custom(False, "impossible", "possible")
        return
    
    # Find components in complement graph (excluding node 1)
    remaining = set(range(2, n+1))
    components = 0
    
    def dfs_complement(start):
        """DFS in complement graph"""
        stack = [start]
        component = []
        
        while stack:
            node = stack.pop()
            if node in remaining:
                remaining.remove(node)
                component.append(node)
                
                # Add all nodes that are NOT connected to current node
                for other in list(remaining):
                    if other not in forbidden[node]:
                        stack.append(other)
        
        return component
    
    # Count components reachable from node 1 in complement graph
    for node in range(2, n+1):
        if node in remaining and node not in forbidden[1]:
            dfs_complement(node)
            components += 1
    
    # Check if solution is possible
    if components > k or len(remaining) > 0:
        print_yes_no_custom(False, "impossible", "possible")
        return
    
    print_yes_no_custom(True, "possible", "impossible")

solve()