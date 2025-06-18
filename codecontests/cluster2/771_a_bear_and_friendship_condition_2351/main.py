#!/usr/bin/env python3

from library import read_ints, DisjointSetUnion, yes_no
from collections import Counter, defaultdict

def main():
    n, m = read_ints()
    dsu = DisjointSetUnion(n+1)  # 1-indexed
    
    # Store all edges
    edges = []
    
    for _ in range(m):
        u, v = read_ints()
        edges.append((u, v))
        dsu.union(u, v)
    
    # Count vertices and edges in each component
    component_edges = defaultdict(int)
    component_vertices = defaultdict(set)
    
    for i in range(1, n+1):
        root = dsu.find(i)
        component_vertices[root].add(i)
    
    for u, v in edges:
        root = dsu.find(u)  # Same as dsu.find(v) since they're connected
        component_edges[root] += 1
    
    # For each component, check if it forms a complete graph
    for root, vertices in component_vertices.items():
        component_size = len(vertices)
        
        # A complete graph with n vertices has n*(n-1)/2 edges
        expected_edges = component_size * (component_size - 1) // 2
        actual_edges = component_edges[root]
        
        if actual_edges != expected_edges:
            print("NO")
            return
    
    print("YES")

if __name__ == "__main__":
    main()