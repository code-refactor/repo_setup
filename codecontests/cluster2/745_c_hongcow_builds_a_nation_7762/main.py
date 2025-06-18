#!/usr/bin/env python3

from library import read_ints, bfs
from collections import defaultdict

def main():
    n, m, k = read_ints()
    government_cities = [c-1 for c in read_ints()]
    
    # Build adjacency list
    adj = [[] for _ in range(n)]
    for _ in range(m):
        u, v = read_ints()
        adj[u-1].append(v-1)
        adj[v-1].append(u-1)
    
    # Find connected components containing government cities
    visited = [False] * n
    components = []
    
    # First, find components containing government cities
    for city in government_cities:
        if not visited[city]:
            component = []
            queue = [city]
            visited[city] = True
            
            while queue:
                current = queue.pop(0)
                component.append(current)
                
                for neighbor in adj[current]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
            
            components.append(component)
    
    # Count cities not in any government component
    not_taken = [i for i in range(n) if not visited[i]]
    
    # Sort components by size (largest first)
    components.sort(key=len, reverse=True)
    
    # Calculate maximum possible edges if we merge all non-government cities
    # with the largest government component
    merged_size = len(components[0]) + len(not_taken)
    max_edges = (merged_size * (merged_size - 1)) // 2
    
    # Add maximum possible edges for other government components
    for i in range(1, len(components)):
        component_size = len(components[i])
        max_edges += (component_size * (component_size - 1)) // 2
    
    # Subtract existing edges
    print(max_edges - m)

if __name__ == "__main__":
    main()
