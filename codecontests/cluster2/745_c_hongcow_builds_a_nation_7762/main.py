#!/usr/bin/env python3

from library import read_ints, Graph
from collections import deque

def solve():
    n, m, k = read_ints()
    
    # Read government cities (1-indexed, convert to 0-indexed)
    gov_cities = read_ints()
    gov_cities = [city - 1 for city in gov_cities]
    
    # Build graph
    graph = Graph(n, directed=False)
    for _ in range(m):
        u, v = read_ints()
        graph.add_edge(u-1, v-1)  # Convert to 0-indexed
    
    # Find which nodes each government city can reach
    gov_components = {}
    remaining_nodes = set(range(n))
    
    for gov in gov_cities:
        remaining_nodes.remove(gov)
        
        # BFS to find all reachable nodes from this government city
        visited = graph.dfs(gov)
        
        # Remove visited nodes from remaining
        for node in visited:
            remaining_nodes.discard(node)
        
        gov_components[gov] = visited
    
    # Convert to list of component sizes and sort by size (largest first)
    component_sizes = [len(component) for component in gov_components.values()]
    component_sizes.sort(reverse=True)
    
    # The largest government component gets all remaining nodes
    largest_component_size = component_sizes[0] + len(remaining_nodes)
    
    # Calculate maximum possible edges
    max_edges = largest_component_size * (largest_component_size - 1) // 2
    
    # Add maximum edges for other components
    for i in range(1, len(component_sizes)):
        size = component_sizes[i]
        max_edges += size * (size - 1) // 2
    
    # Answer is max_edges - current_edges
    print(max_edges - m)

solve()
