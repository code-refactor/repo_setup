#!/usr/bin/env python3

from library import read_ints, read_graph

def solve():
    n, m, k = read_ints()
    
    # Read graph
    graph = read_graph(n, m, directed=False, one_indexed=True)
    
    # Find connected components
    components = graph.connected_components()
    num_components = len(components)
    
    # Special case: if already connected
    if num_components == 1:
        print(1 % k)
        return
    
    # Calculate result using the formula for spanning trees
    # Result = n^(components-2) * product of component sizes
    result = 1
    
    # Multiply by n^(num_components-2)
    for _ in range(num_components - 2):
        result = (result * n) % k
    
    # Multiply by size of each component
    for component in components:
        component_size = len(component)
        result = (result * component_size) % k
    
    print(result)

solve()