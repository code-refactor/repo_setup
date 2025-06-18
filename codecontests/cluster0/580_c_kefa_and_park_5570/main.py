#!/usr/bin/env python3

from library import parse_ints, parse_tree_edges, create_adjacency_list, find_leaves

# Read input
n, m = parse_ints()
cats = parse_ints()

# Read tree edges
edges = parse_tree_edges(n)

# Create adjacency list
adj_list = create_adjacency_list(n, edges)

# BFS to find restaurants (leaves) that Kefa can visit
visited = [False] * n
restaurant_count = 0
queue = [(0, 0)]  # (node, consecutive cats)
i = 0

while i < len(queue):
    node, consecutive_cats = queue[i]
    visited[node] = True
    
    # If we have a cat at current node, increase the count
    # Otherwise reset the count to 0
    if cats[node] == 1:
        current_consecutive = consecutive_cats + 1
    else:
        current_consecutive = 0
    
    # If we haven't exceeded the limit of consecutive cats
    if current_consecutive <= m:
        is_leaf = True
        
        # Check all neighbors
        for neighbor in adj_list[node]:
            if not visited[neighbor]:
                is_leaf = False
                queue.append((neighbor, current_consecutive))
        
        # If this is a leaf (restaurant) and path is valid, count it
        if is_leaf:
            restaurant_count += 1
    
    i += 1

print(restaurant_count)