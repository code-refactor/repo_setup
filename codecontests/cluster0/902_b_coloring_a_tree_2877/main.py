#!/usr/bin/env python3

from library import parse_int, parse_ints
from collections import deque

# Read input
n = parse_int()
parents = parse_ints()
target_colors = parse_ints()

# Create adjacency list (tree representation)
tree = [[] for _ in range(n+1)]  # 1-indexed
for i in range(2, n+1):
    parent = parents[i-2]
    tree[parent].append(i)
    tree[i].append(parent)

# BFS to count the minimum number of coloring operations
min_operations = 0
queue = deque([(1, 0)])  # (node, parent_color)
visited = [False] * (n+1)

while queue:
    node, parent_color = queue.popleft()
    
    if visited[node]:
        continue
    
    visited[node] = True
    
    # Check if we need to color this node (if color is different from parent)
    if target_colors[node-1] != parent_color:
        min_operations += 1
        parent_color = target_colors[node-1]
    
    # Add child nodes to the queue
    for child in tree[node]:
        if not visited[child]:
            queue.append((child, parent_color))

print(min_operations)