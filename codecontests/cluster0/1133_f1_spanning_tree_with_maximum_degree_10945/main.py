#!/usr/bin/env python3

from library import parse_ints
import sys

def dfs(start, visited, adj_list):
    """Depth-first search to mark all nodes reachable from start."""
    stack, counts = [], []
    stack.append(start)
    counts.append(0)
    
    while stack:
        node = stack[-1]
        index = counts[-1]
        visited[node] = 1
        done = True
        
        for j in range(index, len(adj_list[node])):
            neighbor = adj_list[node][j]
            if visited[neighbor] == 0:
                counts[-1] = j + 1
                stack.append(neighbor)
                counts.append(0)
                done = False
                break
                
        if done:
            stack.pop()
            counts.pop()

# Read input
line = input().strip().split()
n, m = map(int, line)
d = n - 1  # In this problem, d is just n-1 (we want maximum degree)

# Initialize adjacency list (1-indexed)
adj = [[] for _ in range(n+1)]

# Read edges and build graph
for _ in range(m):
    x, y = parse_ints()
    adj[x].append(y)
    adj[y].append(x)

# Mark visited nodes (for DFS)
visit = [0] * (n+1)
visit[1] = 1  # Start with node 1

# Store edges in the spanning tree
ans = [0] * m
ct = 0

# Mark nodes already in the spanning tree
mark = [0] * (n+1)
mark[1] = 1  # Node 1 is the initial node

# First, build a spanning forest with node 1 as root
for l in range(len(adj[1])):
    i = adj[1][l]
    if visit[i] == 0:
        dfs(i, visit, adj)
        ans[ct] = [1, i]  # Add edge to spanning tree
        mark[i] = 1
        ct += 1

# Check if degree of node 1 exceeds the limit
if ct > d:
    print("NO")
    sys.exit(0)

# If degree of node 1 is less than d, add more edges to node 1
if ct < d:
    for i in range(len(adj[1])):
        if mark[adj[1][i]] == 0:
            ans[ct] = [1, adj[1][i]]
            mark[adj[1][i]] = 1
            ct += 1
        if ct == d:
            break
    
    # If still can't reach degree d, it's impossible
    if ct < d:
        print("NO")
        sys.exit(0)

# Complete the spanning tree by adding remaining nodes
i = 0
while i < ct:
    k = ans[i][1]
    if visit[k]:
        for j in range(len(adj[k])):
            if mark[adj[k][j]] == 0:
                mark[adj[k][j]] = 1
                ans[ct] = [k, adj[k][j]]
                ct += 1
        visit[k] = 0
    i += 1

# Output the result
print("YES")
for i in range(ct):
    print(*ans[i])