#!/usr/bin/env python3

from library import read_int, read_ints, setup_io
from collections import deque

# Set up fast I/O
input = setup_io()

# Read input
n = read_int()

# Create adjacency list for the tree
adj = [[] for _ in range(n + 1)]

# Read edges
for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

# Read node values
values = read_ints()

# Arrays to track minimum operations needed
plus_ops = [0] * (n + 1)   # Positive operations needed
minus_ops = [0] * (n + 1)  # Negative operations needed
parent = [0] * (n + 1)     # Parent pointers

# BFS to establish tree structure from root (node 1)
queue = deque([1])
visited = [False] * (n + 1)
visited[1] = True
order = []  # To store processing order for bottom-up traversal

# Compute parent pointers and BFS order
while queue:
    node = queue.popleft()
    order.append(node)
    
    for neighbor in adj[node]:
        if not visited[neighbor]:
            visited[neighbor] = True
            parent[neighbor] = node
            queue.append(neighbor)

# Process nodes bottom-up
for node in reversed(order):
    # Calculate the effective shift at this node from previous operations
    shift = minus_ops[node] - plus_ops[node]
    
    # Calculate the value after shift is applied
    adjusted_value = values[node - 1] + shift
    
    # Get parent node
    p = parent[node]
    
    # Update parent's minimum operations
    minus_ops[p] = max(minus_ops[node], minus_ops[p])
    plus_ops[p] = max(plus_ops[node], plus_ops[p])
    
    # If adjusted value is positive, we need more plus operations
    if adjusted_value > 0:
        plus_ops[p] = max(plus_ops[p], plus_ops[node] + adjusted_value)
    # If adjusted value is negative, we need more minus operations
    elif adjusted_value < 0:
        minus_ops[p] = max(minus_ops[p], minus_ops[node] - adjusted_value)

# Print total operations needed
print(plus_ops[0] + minus_ops[0])