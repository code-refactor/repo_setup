#!/usr/bin/env python3

from library import read_ints, read_graph, print_yes_no_custom

def solve():
    n, m = read_ints()
    
    # Read graph (1-indexed)
    graph = read_graph(n, m, directed=False, one_indexed=True)
    
    # Check if graph is connected
    if graph.count_components() != 1:
        print_yes_no_custom(False, "NO", "NO")
        return
    
    # For exactly one cycle in a connected graph:
    # Number of edges must equal number of vertices
    if m != n:
        print_yes_no_custom(False, "NO", "NO") 
        return
    
    # Check if there's exactly one cycle
    if graph.has_cycle():
        print_yes_no_custom(True, "FHTAGN!", "NO")
    else:
        print_yes_no_custom(False, "NO", "NO")

solve()
