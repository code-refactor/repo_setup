#!/usr/bin/env python3

from library import setup_io, read_int
from collections import deque

input = setup_io()

# Constants
MOD = 998244353

# Read input
n, k = map(int, input().split())
adj = [[] for _ in range(n)]

# Read tree edges
for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a - 1].append(b - 1)  # Convert to 0-indexed
    adj[b - 1].append(a - 1)

# BFS to find parent relationships and a processing order
parent = [-1] * n
queue = deque([0])  # Start from vertex 0
process_order = []

while queue:
    node = queue.popleft()
    process_order.append(node)
    
    for neighbor in adj[node]:
        if neighbor != parent[node]:
            parent[neighbor] = node
            queue.append(neighbor)

# Initialize DP array: dp[v][i] = number of ways to cut the subtree rooted at v
# such that the longest path in the subtree has length i
dp = [[1] for _ in range(n)]  # Base case: 1 way to have an empty subtree

def merge(parent_node, child_node):
    """Merge child's DP array into parent's DP array."""
    # Create a new DP array for the result
    result_dp = [0] * max(len(dp[parent_node]), len(dp[child_node]) + 1)
    
    # Combine all possible ways
    for i in range(len(dp[parent_node])):
        for j in range(len(dp[child_node])):
            # Case 1: Connect parent and child (diameter becomes max(j+1, i))
            if j + 1 + i <= k:  # Check if resulting diameter is valid
                result_dp[max(j + 1, i)] = (result_dp[max(j + 1, i)] + dp[parent_node][i] * dp[child_node][j]) % MOD
            
            # Case 2: Cut the edge between parent and child (diameter remains i for parent)
            result_dp[i] = (result_dp[i] + dp[parent_node][i] * dp[child_node][j]) % MOD
    
    # Update parent's DP array
    dp[parent_node] = result_dp

# Process nodes in reverse order (from leaves to root)
for node in reversed(process_order):
    for child in adj[node]:
        if child != parent[node]:  # Skip parent
            merge(node, child)

# Sum all valid configurations (diameter ≤ k)
answer = sum(dp[0][i] for i in range(min(k + 1, len(dp[0])))) % MOD
print(answer)