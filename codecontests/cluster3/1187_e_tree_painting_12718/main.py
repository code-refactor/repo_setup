#!/usr/bin/env python3

import sys
sys.path.append('/home/justinchiu_cohere_com/minicode/codecontests/cluster3')
from library import Utils, TreeBuilder

input = Utils.fast_io()

n = int(input())

# Read edges and build adjacency list
edges = []
for _ in range(n-1):
    a, b = map(int, input().split())
    edges.append((a, b))

# Build 0-indexed adjacency list
G = TreeBuilder.from_edges(n, edges, indexed=1, weighted=False)

F = [0]*n
stk = [0]
visited = [0]*n

while stk:
    x = stk[-1]
    if not visited[x]:
        visited[x] = 1
        for y in G[x]:
            if not visited[y]:
                stk.append(y)
    else:
        x = stk.pop()
        F[x] = 1
        for y in G[x]:                
            F[x] += F[y]

DP = [0]*n
stk = [0]
visited = [0]*n

while stk:
    x = stk[-1]
    if not visited[x]:
        visited[x] = 1
        for y in G[x]:
            if not visited[y]:
                stk.append(y)
    else:
        x = stk.pop()
        DP[x] = F[x]
        for y in G[x]:
            DP[x] += DP[y]

ans = [0]*n
ans[0] = DP[0]
stk = [0]
Z = DP[0]

while stk:
    x = stk.pop()
    for y in G[x]:
        if not ans[y]:
            ay = ans[x] + n - 2 * F[y]
            ans[y] = ay 
            Z = max(Z,ay)
            stk.append(y)

print(Z)