#!/usr/bin/env python3

import sys
sys.path.append('..')
from library import read_int, read_ints

def main():
    n, m = read_ints()
    
    # Store non-edges in a set for each vertex
    non_edges = [set([i]) for i in range(n)]  # Each vertex is non-connected to itself
    
    for _ in range(m):
        u, v = read_ints()
        u, v = u - 1, v - 1  # Convert to 0-indexed
        non_edges[u].add(v)
        non_edges[v].add(u)
    
    # Find connected components using complement graph approach
    unvisited = set(range(n))
    components = []
    
    while unvisited:
        # Start new component with any unvisited vertex
        start = next(iter(unvisited))
        unvisited.remove(start)
        
        # BFS to find all vertices connected to start
        component = [start]
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            # Find all unvisited vertices that are NOT in non_edges[current]
            connected = unvisited - non_edges[current]
            component.extend(connected)
            queue.extend(connected)
            unvisited -= connected
        
        components.append(len(component))
    
    components.sort()
    print(len(components))
    print(" ".join(map(str, components)))

if __name__ == "__main__":
    main()