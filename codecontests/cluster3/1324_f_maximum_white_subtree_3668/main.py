#!/usr/bin/env python3

from library import setup_io, read_int, read_ints

input = setup_io()

# Read input
n = read_int()
colors = read_ints()

# Convert colors to our format: ensure 0 (black) -> -1, 1 (white) -> 1
a = [0] + colors
for i in range(1, n+1):
    if a[i] == 0:
        a[i] = -1

# Read edges
adj = [[] for _ in range(n+1)]
for _ in range(n-1):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

# First DFS: Compute best subtree contribution for each node
dp = [0] * (n+1)

def dfs1(node, parent):
    dp[node] = a[node]  # Start with this node's contribution
    
    for child in adj[node]:
        if child != parent:
            dfs1(child, node)
            dp[node] += max(0, dp[child])  # Only take positive contributions
    
dfs1(1, 0)

# Second DFS: Compute answers for all nodes by re-rooting
ans = [0] * (n+1)

def dfs2(node, parent):
    ans[node] = dp[node]  # Current best subtree value
    
    for child in adj[node]:
        if child != parent:
            # Remove child's contribution from parent
            dp_node_original = dp[node]
            dp_child_original = dp[child]
            
            dp[node] -= max(0, dp[child])
            
            # Add parent's contribution to child (if positive)
            dp[child] += max(0, dp[node])
            
            # Recurse to child
            dfs2(child, node)
            
            # Restore original values
            dp[node] = dp_node_original
            dp[child] = dp_child_original

dfs2(1, 0)

# Print answers for all nodes
print(*ans[1:])