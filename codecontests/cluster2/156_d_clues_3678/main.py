#!/usr/bin/env python3

from library import read_ints

def count_connected_components(n, adj_list):
    """
    Count connected components in an undirected graph and their sizes
    Returns:
        - Number of connected components
        - List of component sizes
    """
    visited = [False] * n
    component_sizes = []
    
    def bfs(start):
        """BFS to find a connected component size"""
        visited[start] = True
        queue = [start]
        size = 0
        
        i = 0
        while i < len(queue):
            node = queue[i]
            size += 1
            i += 1
            
            for neighbor in adj_list[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    queue.append(neighbor)
        
        return size
    
    # Find all components
    component_count = 0
    for i in range(n):
        if not visited[i]:
            size = bfs(i)
            component_sizes.append(size)
            component_count += 1
    
    return component_count, component_sizes

def main():
    # Read input
    n, m, k = read_ints()
    
    # Build adjacency list
    adj_list = [[] for _ in range(n)]
    
    for _ in range(m):
        v, w = read_ints()
        v -= 1  # Convert to 0-indexing
        w -= 1  # Convert to 0-indexing
        adj_list[v].append(w)
        adj_list[w].append(v)
    
    # Count connected components
    component_count, component_sizes = count_connected_components(n, adj_list)
    
    # Special case: already connected
    if component_count == 1:
        print(1 % k)
        return
    
    # Calculate the answer
    # For a tree with n vertices, we need n-1 edges
    # To connect c components, we need c-1 additional edges
    # Number of ways = n^(c-2) * product of component sizes
    
    # Start with n^(c-2)
    answer = 1
    for _ in range(component_count - 2):
        answer = (answer * n) % k
    
    # Multiply by product of component sizes
    for size in component_sizes:
        answer = (answer * size) % k
    
    print(answer)

if __name__ == "__main__":
    main()