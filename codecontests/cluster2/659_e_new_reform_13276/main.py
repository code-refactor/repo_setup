#!/usr/bin/env python3

import sys
sys.path.append('..')
from library import Graph, read_int, read_ints

def main():
    n, m = read_ints()
    graph = Graph(n)
    
    for _ in range(m):
        x, y = read_ints()
        graph.add_edge(x - 1, y - 1)  # Convert to 0-indexed
    
    components = graph.connected_components()
    separate_cities = 0
    
    for component in components:
        # For each component, we need to check if it has a cycle
        # If it has a cycle, we can orient all edges so no city is separate
        # If it's a tree, exactly one city must be separate (the root)
        
        # Count edges in this component
        edge_count = 0
        for vertex in component:
            edge_count += len(graph.neighbors(vertex))
        edge_count //= 2  # Each edge is counted twice
        
        # If edges == vertices - 1, it's a tree (no cycle)
        # If edges >= vertices, it has a cycle
        if edge_count == len(component) - 1:
            # Tree component - needs 1 separate city
            separate_cities += 1
        # If it has a cycle, no separate cities needed
    
    print(separate_cities)

if __name__ == "__main__":
    main()