#!/usr/bin/env python3

from library import read_ints
from collections import defaultdict, deque

def dfs(node, weight_1_edges, visited, n):
    """DFS on the complement graph (edges with weight 0)"""
    stack = [node]
    visited[node] = True
    
    while stack:
        current = stack.pop()
        # For each node, check all other nodes
        for next_node in range(1, n+1):
            # If the node is not visited, not the same as current, and not connected by weight-1 edge
            if not visited[next_node] and next_node != current and next_node not in weight_1_edges[current]:
                visited[next_node] = True
                stack.append(next_node)
    
    return

n, m = read_ints()

# Read edges with weight 1
weight_1_edges = defaultdict(set)
for _ in range(m):
    a, b = read_ints()
    weight_1_edges[a].add(b)
    weight_1_edges[b].add(a)

# Count connected components using DFS
visited = [False] * (n+1)
component_count = 0

for i in range(1, n+1):
    if not visited[i]:
        component_count += 1
        dfs(i, weight_1_edges, visited, n)

print(component_count - 1)