#!/usr/bin/env python3

from library import read_int, setup_io
from collections import deque

# Set up fast I/O
input = setup_io()

# Read input
n = read_int()

# Create adjacency list for the tree
adj = [[] for _ in range(n + 1)]
for _ in range(1, n):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

# BFS to establish tree structure from root (node 1)
queue = deque([1])
depth = [None] * (n + 1)
depth[1] = 0
processing_order = [1]  # Store nodes in BFS order for bottom-up processing

# Perform BFS to compute depths and directed tree structure
while queue:
    node = queue.popleft()
    for child in list(adj[node]):  # Use list() to avoid modifying during iteration
        if depth[child] is None:
            queue.append(child)
            processing_order.append(child)
            depth[child] = depth[node] + 1
            # Remove parent from child's adjacency list to make the tree directed
            adj[child].remove(node)

# DP arrays
min_val = [0] * (n + 1)  # Minimum possible value when optimal play
max_val = [0] * (n + 1)  # Maximum possible value when optimal play
leaf_count = 0           # Count number of leaves

# Process nodes in reverse BFS order (bottom-up)
for node in reversed(processing_order):
    if not adj[node]:  # Leaf node
        min_val[node] = 1
        max_val[node] = 1
        leaf_count += 1
    elif depth[node] % 2 == 0:  # Even depth (minimizing player's turn)
        # Minimizer wants to minimize, so takes minimum among children's maximums
        min_sum = 0
        max_min = float('inf')
        
        # Sum of minimums for min_val
        for child in adj[node]:
            min_sum += min_val[child]
            
        # Minimum of maximums for max_val
        for child in adj[node]:
            max_min = min(max_min, max_val[child])
            
        min_val[node] = min_sum
        max_val[node] = max_min
    else:  # Odd depth (maximizing player's turn)
        # Maximizer wants to maximize, so takes maximum among children's minimums
        min_min = float('inf')
        max_sum = 0
        
        # Minimum of minimums for min_val
        for child in adj[node]:
            min_min = min(min_min, min_val[child])
            
        # Sum of maximums for max_val
        for child in adj[node]:
            max_sum += max_val[child]
            
        min_val[node] = min_min
        max_val[node] = max_sum

# Print results
# Maximum value: leaf_count + 1 - max_val[root] (this is because of the numbering 1 to m)
# Minimum value: min_val[root]
print(leaf_count + 1 - max_val[1], min_val[1])
