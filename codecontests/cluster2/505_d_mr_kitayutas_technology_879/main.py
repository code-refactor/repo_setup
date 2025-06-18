#!/usr/bin/env python3

from library import read_ints, DisjointSetUnion
from sys import setrecursionlimit

def main():
    # Set high recursion limit for DFS
    setrecursionlimit(100500)
    
    n, m = read_ints()
    n += 1  # Adjust for 1-indexed vertices
    
    # Initialize data structures
    in_degree = [0] * n  # Number of incoming edges for each vertex
    adj_list = [[] for _ in range(n)]  # Adjacency list for the graph
    dsu = DisjointSetUnion(n)  # DSU to track connected components
    
    # Read edges and update data structures
    for _ in range(m):
        a, b = read_ints()
        adj_list[a].append(b)  # Add edge a -> b
        in_degree[b] += 1  # Increment in-degree of b
        dsu.union(a, b)  # Union vertices in DSU
    
    # Topological sorting to identify vertices with no cycles
    queue = [a for a, degree in enumerate(in_degree) if degree == 0]
    for a in queue:
        for b in adj_list[a]:
            in_degree[b] -= 1
            if in_degree[b] == 0:
                queue.append(b)
    
    # Mark components with cycles
    has_cycle = [False] * n
    for vertex, degree in enumerate(in_degree):
        if degree > 0:  # Vertices with remaining in-degree are part of cycles
            root = dsu.find(vertex)
            has_cycle[root] = True
    
    # Count components without cycles
    count = 0
    for i in range(n):
        if i == dsu.find(i) and not has_cycle[i]:
            count += 1
    
    # The answer is n - count
    print(n - count)

if __name__ == '__main__':
    main()
