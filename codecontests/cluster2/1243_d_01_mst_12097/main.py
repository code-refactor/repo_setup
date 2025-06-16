#!/usr/bin/env python3

from library import read_ints

def solve():
    n, m = read_ints()
    
    # Build adjacency sets
    adj = [set() for _ in range(n)]
    for _ in range(m):
        a, b = read_ints()
        a, b = a-1, b-1
        adj[a].add(b)
        adj[b].add(a)
    
    # Find connected components in the complement graph
    # Two nodes are connected in complement if they are NOT connected in original
    components = 0
    unused = set(range(n))
    
    while unused:
        # Start a new component
        current_component = {unused.pop()}
        
        # Keep expanding the component
        while current_component:
            node = current_component.pop()
            # Find all unused nodes that are NOT connected to this node
            neighbors_in_complement = {j for j in unused if j not in adj[node]}
            unused.difference_update(neighbors_in_complement)
            current_component.update(neighbors_in_complement)
        
        components += 1
    
    # Answer is components - 1 (minimum edges to connect all components)
    print(components - 1)

solve()