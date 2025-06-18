#!/usr/bin/env python3

from library import read_int, read_ints
from collections import UserDict

class Tree(UserDict):
    def __init__(self, g):
        super().__init__()
        for name, value in enumerate(g, 1):
            self[value] = name

    def __setitem__(self, name, value):
        if name in self:
            if value is not None:
                self[name].add(value)
                self[value] = None
        else:
            if value is None:
                super().__setitem__(name, set())
            else:
                super().__setitem__(name, {value})
                self[value] = None

# Read input
n = read_int()
parent_list = read_ints()  # Parent of each node (0-indexed)
colors = read_ints()       # Colors of nodes (0 for white, 1 for black)

# Create tree from parent list
tree = Tree(parent_list)

# DP array: t[v] = (white_ways, black_ways)
# white_ways: ways to get 0 black nodes in this subtree
# black_ways: ways to get exactly 1 black node in this subtree
t = [()] * n

def dfs(v):
    """Iterative DFS with post-order processing for DP on tree"""
    stack = [v]
    visited = set()

    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            stack.append(v)  # Add back to process after children
            stack.extend(tree[v])  # Add children
        else:
            # Initialize with base case
            t[v] = (1, colors[v])
            
            # Process each child
            for u in tree[v]:
                # Calculate new values exactly as in original code
                t[v] = (
                    (t[v][0] * t[u][1] + t[v][0] * t[u][0] * (not colors[u])) % (10**9 + 7),
                    (t[v][1] * t[u][1] + t[v][0] * t[u][1] * (not colors[v])
                    + t[v][1] * t[u][0] * (not colors[u])) % (10**9 + 7)
                )

# Start DFS from root (node 0)
dfs(0)

# Print the number of ways to have exactly 1 black node in each component
print(t[0][1])