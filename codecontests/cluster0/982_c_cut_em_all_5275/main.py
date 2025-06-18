#!/usr/bin/env python3

from library import parse_int, parse_ints, create_adjacency_list
import sys

# Increase recursion limit for large inputs
sys.setrecursionlimit(300000)

# Read input
n = parse_int()

# If n is odd, it's impossible to have all even-sized components
if n % 2 != 0:
    print(-1)
    sys.exit(0)

# Read edges and create adjacency list
edges = []
for _ in range(n - 1):
    u, v = parse_ints()
    u -= 1  # Convert to 0-indexed
    v -= 1
    edges.append((u, v))

# Create adjacency list
adj_list = create_adjacency_list(n, edges)

# DFS to compute subtree sizes
def dfs(node, parent):
    subtree_size = 1  # Count the node itself
    for neighbor in adj_list[node]:
        if neighbor != parent:
            subtree_size += dfs(neighbor, node)
    
    subtree_sizes[node] = subtree_size
    return subtree_size

# Store subtree sizes
subtree_sizes = [0] * n

# Run DFS from root (node 0)
dfs(0, -1)

# Count edges that can be removed
# We can remove an edge if the subtree below it has an even size
removable_edges = 0
for i in range(1, n):  # Skip the root
    if subtree_sizes[i] % 2 == 0:
        removable_edges += 1

print(removable_edges)