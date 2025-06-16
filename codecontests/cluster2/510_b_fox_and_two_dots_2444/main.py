#!/usr/bin/env python3

from library import read_ints, Graph, print_yes_no_custom

row, col = read_ints()
grid = []
for _ in range(row):
    grid.append(input())

graph = Graph(row * col)

for i in range(row):
    for j in range(col):
        current = i * col + j
        
        if j + 1 < col and grid[i][j] == grid[i][j + 1]:
            graph.add_edge(current, current + 1)
        
        if i + 1 < row and grid[i][j] == grid[i + 1][j]:
            graph.add_edge(current, current + col)

print_yes_no_custom(graph.has_cycle(), "Yes", "No")
