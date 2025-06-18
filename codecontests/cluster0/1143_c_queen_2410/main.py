#!/usr/bin/env python3

from library import parse_int, parse_ints

# Read input
n = parse_int()

parent = [0] * n  # Stores the parent of each node
respect = [0] * n  # Stores whether each node respects its ancestors (0) or not (1)
children = [[] for _ in range(n)]  # List of children for each node
has_respectful_child = [False] * n  # Stores whether node has at least one child that respects it
root = -1

# Read parent-child relationships and respect values
for i in range(n):
    p, c = parse_ints()
    
    parent[i] = p
    respect[i] = c  # c=1 means the child doesn't respect its ancestors, c=0 means it respects
    
    if p == -1:
        root = i  # This is the root node
        continue
    
    # Connect parent to child
    children[p-1].append(i)

# Update has_respectful_child for each node
for i in range(n):
    if parent[i] != -1 and respect[i] == 0:  # If this node respects its parent
        has_respectful_child[parent[i]-1] = True

# Find nodes to delete
# A node should be deleted if:
# 1. It's not the root
# 2. It doesn't respect its ancestors (respect[i] = 1)
# 3. None of its children respect it (has_respectful_child[i] = False)
nodes_to_delete = []
for i in range(n):
    if i == root:
        continue
    if respect[i] == 1 and not has_respectful_child[i]:
        nodes_to_delete.append(i+1)  # +1 for 1-indexing

# Print result
if nodes_to_delete:
    print(*nodes_to_delete)
else:
    print(-1)