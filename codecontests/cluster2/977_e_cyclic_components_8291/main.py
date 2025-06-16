#!/usr/bin/env python3

import sys
sys.path.append('..')
from library import Graph, read_int, read_ints

def is_cycle_component(graph, component):
    """Check if a connected component is a cycle"""
    # A component is a cycle if:
    # 1. Every vertex has exactly degree 2
    # 2. The component is connected (already guaranteed)
    for vertex in component:
        if len(graph.neighbors(vertex)) != 2:
            return False
    return len(component) >= 3  # Cycles must have at least 3 vertices

n, m = read_ints()
graph = Graph(n)

for _ in range(m):
    u, v = read_ints()
    graph.add_edge(u - 1, v - 1)  # Convert to 0-indexed

components = graph.connected_components()
cycle_count = 0

for component in components:
    if is_cycle_component(graph, component):
        cycle_count += 1

print(cycle_count)

  		 		 	   	 				 	     	   	