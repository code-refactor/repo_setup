#!/usr/bin/env python3

from library import setup_io, read_int

input = setup_io()

n = read_int()
G = [[] for _ in range(n)]

# Read tree edges
for _ in range(n-1):
    a, b = map(int, input().split())
    G[a-1].append(b-1)
    G[b-1].append(a-1)

# First DFS: Compute subtree sizes
F = [0] * n
stk = [0]
visited = [0] * n

while stk:
    x = stk[-1]
    if not visited[x]:
        visited[x] = 1
        for y in G[x]:
            if not visited[y]:
                stk.append(y)
    else:
        x = stk.pop()
        F[x] = 1  # Count the node itself
        for y in G[x]:                
            F[x] += F[y]  # Add subtree sizes

# Second DFS: Compute cumulative sum of subtree sizes
DP = [0] * n
stk = [0]
visited = [0] * n

while stk:
    x = stk[-1]
    if not visited[x]:
        visited[x] = 1
        for y in G[x]:
            if not visited[y]:
                stk.append(y)
    else:
        x = stk.pop()
        DP[x] = F[x]  # Start with node's subtree size
        for y in G[x]:
            DP[x] += DP[y]  # Add children's DP values

# Third pass: Compute answer for all possible root nodes
ans = [0] * n
ans[0] = DP[0]  # Initial value for root 0
stk = [0]
Z = DP[0]  # Best answer so far

while stk:
    x = stk.pop()
    for y in G[x]:
        if not ans[y]:  # If node hasn't been processed
            # Rerooting formula: ans[y] = ans[x] + n - 2 * F[y]
            ay = ans[x] + n - 2 * F[y]
            ans[y] = ay 
            Z = max(Z, ay)  # Update best answer
            stk.append(y)

print(Z)