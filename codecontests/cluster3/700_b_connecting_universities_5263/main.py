#!/usr/bin/env python3

from library import read_int_tuple, bootstrap

@bootstrap
def dfs(node, parent):
    for neighbor, _ in adj[node]:
        if neighbor != parent:
            yield dfs(neighbor, node)
            univ_count[node] += univ_count[neighbor]
            dp[node] += dp[neighbor] + min(univ_count[neighbor], total_univ - univ_count[neighbor])
    yield

# Read input
n, k = read_int_tuple()
total_univ = 2 * k
universities = list(map(int, input().split()))

# Initialize arrays
univ_count = [0] * (n + 1)
dp = [0] * (n + 1)

# Mark university locations
for univ in universities:
    univ_count[univ] = 1

# Create adjacency list manually
adj = [[] for _ in range(n + 1)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    adj[u].append((v, 1))  # Weight 1 for all edges
    adj[v].append((u, 1))

# Run DFS to compute result
dfs(1, -1)

# Output the result
print(dp[1])