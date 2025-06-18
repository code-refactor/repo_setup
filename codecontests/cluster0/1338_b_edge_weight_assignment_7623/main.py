#!/usr/bin/env python3

from library import parse_int, parse_tree_edges, create_adjacency_list, find_leaves, dfs_with_stack

n = parse_int()

# Read tree edges
edges = parse_tree_edges(n)

# Create adjacency list
adj_list = create_adjacency_list(n, edges)

# Calculate leaf depths using DFS
leaf_depths = []
visited = {0: True}
stack = [(0, 0)]  # (node, depth)

while stack:
    node, depth = stack.pop()
    is_leaf = True
    
    for neighbor in adj_list[node]:
        if neighbor not in visited:
            visited[neighbor] = True
            is_leaf = False
            stack.append((neighbor, depth + 1))
    
    if is_leaf:
        leaf_depths.append(depth)

# Calculate MAX (number of distinct weights needed)
unique_edges = set()
for a, b in edges:
    # Replace leaf nodes with -1
    if len(adj_list[a]) == 1:
        a = -1
    if len(adj_list[b]) == 1:
        b = -1
    
    # Ensure consistent ordering
    if a > b:
        a, b = b, a
    
    unique_edges.add((a, b))

MAX = len(unique_edges)

# Calculate MIN (minimum number of distinct weights)
if len(adj_list[0]) == 1:  # Root is a leaf
    MIN = 1 if all(depth % 2 == 0 for depth in leaf_depths) else 3
else:
    MIN = 1 if all(depth % 2 == 0 for depth in leaf_depths) or all(depth % 2 == 1 for depth in leaf_depths) else 3

print(MIN, MAX)