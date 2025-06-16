#!/usr/bin/env python3

from library import read_ints, Graph, print_yes_no

def solve():
    n, m = read_ints()
    
    graph = Graph(n, directed=False)
    for _ in range(m):
        u, v = read_ints()
        graph.add_edge(u-1, v-1)  # Convert to 0-indexed
    
    # Find connected components
    components = graph.connected_components()
    num_components = len(components)
    
    # Check maximum degree
    max_degree = 0
    for i in range(n):
        max_degree = max(max_degree, len(graph.neighbors(i)))
    
    # For a forest: n - m should equal number of components
    # Also, max degree should be <= 2 for valid forest (unless special case)
    if n - m != num_components or max_degree > 2:
        # Special case: exactly one cycle (n == m, one component, max degree 2)
        if n == m and num_components == 1 and max_degree == 2:
            print_yes_no(True)
            print(0)
        else:
            print_yes_no(False)
    else:
        print_yes_no(True)
        print(n - m)  # Number of edges to add
        
        # Find leaves (degree 1) and isolated nodes (degree 0) in each component
        leaves_by_component = {}
        
        for comp_idx, component in enumerate(components):
            leaves = []
            for node in component:
                degree = len(graph.neighbors(node))
                if degree == 1:
                    leaves.append(node + 1)  # Convert back to 1-indexed
                elif degree == 0:
                    leaves.extend([node + 1, node + 1])  # Add twice for isolated nodes
            leaves_by_component[comp_idx] = leaves
        
        # Connect components by pairing leaves from different components
        used_leaves = set()
        
        for i in range(len(components)):
            if i in used_leaves:
                continue
            
            leaves_i = [leaf for leaf in leaves_by_component[i] if leaf not in used_leaves]
            if not leaves_i:
                continue
                
            for j in range(i + 1, len(components)):
                if j in used_leaves:
                    continue
                    
                leaves_j = [leaf for leaf in leaves_by_component[j] if leaf not in used_leaves]
                if not leaves_j:
                    continue
                
                # Connect first available leaf from each component
                print(leaves_i[0], leaves_j[0])
                used_leaves.add(leaves_i[0])
                used_leaves.add(leaves_j[0])
                used_leaves.add(i)
                used_leaves.add(j)
                break
        
        # Connect remaining leaves within the same component
        for comp_idx, leaves in leaves_by_component.items():
            available_leaves = [leaf for leaf in leaves if leaf not in used_leaves]
            for k in range(0, len(available_leaves) - 1, 2):
                if k + 1 < len(available_leaves):
                    print(available_leaves[k], available_leaves[k + 1])

solve()