#!/usr/bin/env python3

from library import Graph, yes_no
from sys import setrecursionlimit
setrecursionlimit(10**6)

def has_cycle(g, start, prev, visited):
    visited[start] = True
    
    for neighbor in g.neighbors(start):
        if not visited[neighbor]:
            if has_cycle(g, neighbor, start, visited):
                return True
        elif neighbor != prev:
            return True
            
    return False

# Process the input
row, col = map(int, input().split())
rows = [input() for _ in range(row)]

# Create graph with row*col vertices
graph = Graph(row * col)

# Connecting nodes with same color
for i in range(row):
    for j in range(col):
        node_id = i * col + j
        color = rows[i][j]
        
        # Check right neighbor
        if j + 1 < col and rows[i][j+1] == color:
            graph.add_edge(node_id, node_id + 1)
            
        # Check bottom neighbor
        if i + 1 < row and rows[i+1][j] == color:
            graph.add_edge(node_id, node_id + col)

# Check for cycle
visited = [False] * (row * col)
cycle_found = False

for i in range(row * col):
    if not visited[i]:
        if has_cycle(graph, i, -1, visited):
            cycle_found = True
            break

print(yes_no(cycle_found, "Yes", "No"))
