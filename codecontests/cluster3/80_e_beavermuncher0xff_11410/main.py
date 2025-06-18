#!/usr/bin/env python3

from library import read_int, read_ints

# Read input
n = read_int()
beaver = read_ints()
adj = [[] for _ in range(n)]
deg = [0] * n

# Build the tree
for _ in range(n - 1):
    u, v = read_ints()
    adj[u - 1].append(v - 1)
    adj[v - 1].append(u - 1)
    deg[u - 1] += 1
    deg[v - 1] += 1

# Get starting vertex
start = read_int() - 1
deg[start] += 1000000  # Mark start vertex

# Handle edge case
if n == 1:
    print(0)
    exit()

# Initialize DP array
dp = [0] * n

# Process leaf nodes first and work up towards the root
stack = [i for i in range(n) if i != start and deg[i] == 1]
while stack:
    v = stack.pop()
    deg[v] = 0
    child = []
    child_dp = []

    for dest in adj[v]:
        if deg[dest] == 0:
            child.append(dest)
            child_dp.append(dp[dest])
        else:
            deg[dest] -= 1
            if deg[dest] == 1:
                stack.append(dest)

    # Sort children DP values in descending order
    child_dp.sort(reverse=True)
    
    # Calculate optimal number of visits
    x = min(beaver[v] - 1, len(child))
    dp[v] = 1 + sum(child_dp[:x]) + x
    beaver[v] -= x + 1
    
    # Process remaining beavers
    for c in child:
        x = min(beaver[v], beaver[c])
        beaver[v] -= x
        dp[v] += 2 * x

# Process the starting vertex separately
x = min(beaver[start], len(adj[start]))
child_dp = sorted((dp[v] for v in adj[start]), reverse=True)
ans = sum(child_dp[:x]) + x
beaver[start] -= x

# Process remaining beavers at the start vertex
for c in adj[start]:
    x = min(beaver[start], beaver[c])
    beaver[start] -= x
    ans += 2 * x

print(ans)
