#!/usr/bin/env python3

from library import parse_ints, create_adjacency_list
import sys

# Handle different input formats
first_line = input().strip()
if ' ' in first_line:
    n, _ = map(int, first_line.split())
else:
    n = int(first_line)

# Read colors
a = parse_ints()  # Node colors (0, 1, or 2)

# Read edges and build the tree
edges = []
for i in range(n-1):
    v1, v2 = parse_ints()
    # Convert to 0-indexed
    v1 -= 1
    v2 -= 1
    edges.append((v1, v2))

# Create adjacency list
adj_list = create_adjacency_list(n, edges)

# Initialize state variables
count = [[0, 0] for _ in range(n)]  # Count of color 1 and 2 in each subtree
total = [a.count(1), a.count(2)]    # Total count of colors in the tree
answer = 0                         # Result counter

# Define DFS states for the iterative approach
OBSERVE = 0  # First visit to a node (pre-order)
CHECK = 1    # Second visit to a node (post-order)

# Perform iterative DFS
stack = [(OBSERVE, 0, -1)]  # (state, vertex, parent)

while stack:
    state, vertex, parent = stack.pop()
    
    if state == OBSERVE:
        # On first visit, push a CHECK state for this node
        # and OBSERVE states for all children
        stack.append((CHECK, vertex, parent))
        for child in adj_list[vertex]:
            if child != parent:
                stack.append((OBSERVE, child, vertex))
    else:
        # On second visit, process the node
        # Accumulate color counts from children
        for child in adj_list[vertex]:
            if child != parent:
                # Check if cutting the edge to this child would
                # create two valid components
                if (count[child][0] == total[0] and count[child][1] == 0) or \
                   (count[child][1] == total[1] and count[child][0] == 0):
                    answer += 1
                    
                # Add child's counts to current node
                count[vertex][0] += count[child][0]
                count[vertex][1] += count[child][1]
 
        # Add current node's color to its count
        if a[vertex] == 1 or a[vertex] == 2:
            count[vertex][a[vertex]-1] += 1
 
print(answer)
