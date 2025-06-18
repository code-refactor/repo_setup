#!/usr/bin/env python3

from library import parse_int
from collections import deque

# Read the number of employees
n = parse_int()

# Create a graph where an edge from a to b means 'a is the manager of b'
managers = []
children = [[] for _ in range(n)]
roots = []

# Read the immediate managers
for i in range(n):
    manager = parse_int()
    managers.append(manager)
    
    if manager == -1:
        # This employee has no manager (is a root)
        roots.append(i)
    else:
        # Adjust to 0-indexed
        manager -= 1
        # Add the employee to the manager's children
        children[manager].append(i)

# Find the maximum depth of any tree in the forest
def find_max_depth():
    max_depth = 0
    
    for root in roots:
        # BFS to find the depth of this tree
        queue = deque([(root, 1)])  # (node, depth)
        while queue:
            node, depth = queue.popleft()
            max_depth = max(max_depth, depth)
            
            for child in children[node]:
                queue.append((child, depth + 1))
    
    return max_depth

# The minimum number of groups needed is the maximum depth of any tree
print(find_max_depth())