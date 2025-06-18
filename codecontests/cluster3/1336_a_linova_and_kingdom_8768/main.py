#!/usr/bin/env python3

from library import setup_io, read_int

input = setup_io()

def dfs(x, a):
    """
    DFS to compute subtree sizes and depths.
    
    Args:
        x: Current node
        a: Current depth
        
    Returns:
        Size of subtree rooted at x
    """
    v[x] = 1  # Mark as visited
    d[x] = a  # Set depth
    c = 0     # Initialize subtree size
    
    for i in adj[x]:
        if not v[i]:
            # Add subtree size plus the node itself
            c += dfs(i, a + 1) + 1
            
    l[x] = c  # Store subtree size
    return l[x]

# Read input
n, k = map(int, input().split())

# Initialize arrays
v = [0] * (n + 1)  # Visited
l = [0] * (n + 1)  # Subtree sizes
d = [0] * (n + 1)  # Depths
adj = [[] for _ in range(n + 1)]  # Adjacency list

# Read edges
for i in range(n - 1):
    x, y = map(int, input().split())
    adj[x].append(y)
    adj[y].append(x)

# Run DFS to compute subtree sizes and depths
dfs(1, 0)

# For each node, compute its contribution value
# This is the subtree size minus depth (l[i] - d[i])
contributions = []
for i in range(1, n + 1):
    contributions.append(l[i] - d[i])

# Sort contributions in descending order
contributions.sort(reverse=True)

# Choose the largest n-k contributions
# These correspond to nodes that should be industrial
print(sum(contributions[:n - k]))