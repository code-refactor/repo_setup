#!/usr/bin/env python3

import sys
sys.path.append('..')
from library import Graph, read_int, read_ints

def main():
    n, m = read_ints()
    graph = Graph(n)
    
    for _ in range(m):
        a, b = read_ints()
        graph.add_edge(a - 1, b - 1)  # Convert to 0-indexed
    
    components = graph.connected_components()
    bench_students = 0
    
    for component in components:
        size = len(component)
        
        # Check if component forms a cycle (odd cycle can't be 2-colored)
        # Count edges in this component
        edge_count = 0
        for vertex in component:
            edge_count += len(graph.neighbors(vertex))
        edge_count //= 2  # Each edge is counted twice
        
        # If it's a cycle (edges == vertices) and odd-sized, remove 1 student
        if edge_count == size and size % 2 == 1:
            bench_students += 1
        # If it's a path or tree (edges == vertices - 1), no students removed
        # Component can always be 2-colored if it's not an odd cycle
    
    # After removing students from odd cycles, check if remaining is even
    remaining = n - bench_students
    if remaining % 2 == 1:
        bench_students += 1
    
    print(bench_students)

if __name__ == "__main__":
    main()