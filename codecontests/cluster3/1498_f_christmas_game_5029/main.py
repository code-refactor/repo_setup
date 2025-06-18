#!/usr/bin/env python3

from library import setup_io, read_int, read_ints
from collections import deque

input = setup_io()

# Read input
n, k = map(int, input().split())
adj = [[] for _ in range(n)]

# Read tree edges
for _ in range(n - 1):
    x, y = map(int, input().split())
    x -= 1  # Convert to 0-indexed
    y -= 1
    adj[x].append(y)
    adj[y].append(x)

# Read number of presents on each node
presents = read_ints()

# BFS to find a topological ordering and parent relationships
parent = list(range(n))  # Initial parent is itself
visit_order = []
queue = deque([0])  # Start BFS from node 0

while queue:
    node = queue.popleft()
    visit_order.append(node)
    
    for neighbor in adj[node]:
        if neighbor != parent[node]:
            parent[neighbor] = node
            queue.append(neighbor)

# First DP: Compute XOR values for each node and each distance
dp = [[0] * (2 * k) for _ in range(n)]

# Process nodes in reverse topological order (bottom-up)
for node in reversed(visit_order):
    # Base case: XOR with node's own presents
    dp[node][0] ^= presents[node]
    
    # Combine with children's values
    for child in adj[node]:
        if child != parent[node]:
            for dist in range(2 * k):
                dp[node][(dist + 1) % (2 * k)] ^= dp[child][dist]

# Second DP: Re-root the tree and compute answers
answers = [None] * n

# Process nodes in topological order (top-down)
for node in visit_order:
    if node == 0:  # Root case
        # For the root, we just need to XOR values at distances k to 2k-1
        result = 0
        for dist in range(k, 2 * k):
            result ^= dp[node][dist]
        answers[node] = min(result, 1)  # 1 if non-zero (Alice wins), 0 otherwise
    else:
        # For non-root nodes, we need to combine with parent's values
        # First, make a copy of parent's DP values
        parent_dp = [dp[parent[node]][dist] for dist in range(2 * k)]
        
        # Remove this node's contribution from parent
        for dist in range(2 * k):
            parent_dp[(dist + 1) % (2 * k)] ^= dp[node][dist]
        
        # Add parent's contribution to this node
        for dist in range(2 * k):
            dp[node][(dist + 1) % (2 * k)] ^= parent_dp[dist]
        
        # Calculate the answer for this node
        result = 0
        for dist in range(k, 2 * k):
            result ^= dp[node][dist]
        answers[node] = min(result, 1)

# Print the answers
print(*answers)