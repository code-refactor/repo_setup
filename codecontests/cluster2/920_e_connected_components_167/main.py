#!/usr/bin/env python3

from library import read_ints

def main():
    n, m = read_ints()
    
    # Store non-edges - for each vertex, the set of vertices NOT connected to it
    # (including itself)
    non_edges = [{i} for i in range(n)]
    
    for _ in range(m):
        u, v = read_ints()
        u, v = u-1, v-1
        # Add both vertices to each other's non-edge set
        non_edges[u].add(v)
        non_edges[v].add(u)
    
    # Remaining vertices to process
    remaining = set(range(n))
    component_sizes = []
    
    # Process each connected component
    while remaining:
        # Start with any unprocessed vertex
        start = next(iter(remaining))
        remaining.remove(start)
        
        # DFS to find all vertices in this component
        stack = [start]
        component_size = 1
        
        while stack:
            current = stack.pop()
            
            # Find unprocessed vertices connected to current
            # (those NOT in non_edges[current])
            connected = remaining - non_edges[current]
            
            # Add these to component size and stack
            component_size += len(connected)
            stack.extend(connected)
            
            # Remove processed vertices from remaining
            remaining &= non_edges[current]
        
        component_sizes.append(component_size)
    
    # Sort component sizes and print result
    component_sizes.sort()
    print(len(component_sizes))
    print(" ".join(map(str, component_sizes)))

if __name__ == "__main__":
    main()