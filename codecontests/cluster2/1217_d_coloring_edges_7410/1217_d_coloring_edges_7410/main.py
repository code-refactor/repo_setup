#!/usr/bin/env python3

from library import read_ints

def dfs(node, adj, visited, in_dfs_path):
    """Check if there's a cycle in a directed graph starting from node"""
    if node in in_dfs_path:
        return True
    
    if visited[node]:
        return False
    
    visited[node] = True
    in_dfs_path.add(node)
    
    for neighbor in adj[node]:
        if dfs(neighbor, adj, visited, in_dfs_path):
            return True
    
    in_dfs_path.remove(node)
    return False

n, m = read_ints()
adj = [[] for _ in range(n+1)]
has_parent = [False] * (n+1)
edges = []

for _ in range(m):
    u, v = read_ints()
    adj[u].append(v)
    has_parent[v] = True
    edges.append((u, v))

# Check if the graph has a cycle
has_cycle = False
visited = [False] * (n+1)

for i in range(1, n+1):
    if not has_parent[i] and dfs(i, adj, visited, set()):
        has_cycle = True
        break

for i in range(1, n+1):
    if has_parent[i] and not visited[i]:
        has_cycle = True
        break

if has_cycle:
    # If there's a cycle, use 2 colors
    # Color forward edges (u < v) with color 1, backward edges with color 2
    colors = []
    for u, v in edges:
        colors.append('1' if u < v else '2')
    
    print(2)
    print(' '.join(colors))
else:
    # If there's no cycle, use 1 color
    print(1)
    print(' '.join(['1'] * m))