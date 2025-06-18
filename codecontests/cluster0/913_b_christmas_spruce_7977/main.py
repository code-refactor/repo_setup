#!/usr/bin/env python3

from library import parse_int

# Read the number of vertices
n = parse_int()

# Create adjacency list for children of each node
children = [[] for _ in range(n + 1)]

# Read parent-child relationships
for i in range(2, n + 1):
    parent = parse_int()
    children[parent].append(i)

# For each non-leaf node, check if it has at least 3 leaf children
for i in range(1, n + 1):
    # Skip if this node has no children (it's a leaf)
    if not children[i]:
        continue
        
    # Count leaf children
    leaf_children_count = sum(1 for child in children[i] if not children[child])
    
    # If it's a non-leaf node with less than 3 leaf children, it's not a spruce
    if leaf_children_count < 3:
        print("No")
        exit()

# If all non-leaf nodes have at least 3 leaf children, it's a spruce
print("Yes")