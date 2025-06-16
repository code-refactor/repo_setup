#!/usr/bin/env python3

from library import ints, int_inp
from collections import deque

n = int_inp()

# Build tree from parent array (1-indexed)
children = [[] for _ in range(n+1)]
parent_list = list(ints())
for i in range(2, n+1):
    parent = parent_list[i-2]
    children[parent].append(i)

# Read colors
colors = list(ints())

# BFS to count color changes
queue = deque([1])
result = 0

while queue:
    node = queue.popleft()
    
    if node == 1:
        parent_color = 0
    else:
        parent_node = parent_list[node-2]
        parent_color = colors[parent_node-1]
    
    if parent_color != colors[node-1]:
        result += 1
    
    for child in children[node]:
        queue.append(child)

print(result)
