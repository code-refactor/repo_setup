from library import *

n = int_inp()
edges = []
for _ in range(n - 1):
    a, b = ints()
    edges.append((a-1, b-1))

# Build graph using library
graph = adj_list(n, edges)

# Calculate MAX - edges between non-leaf nodes
edge_set = set()
for a, b in edges:
    if len(graph[a]) == 1:
        a = -1
    if len(graph[b]) == 1:
        b = -1
    if a > b:
        a, b = b, a
    edge_set.add((a, b))

MAX = len(edge_set)

# Calculate MIN using DFS to find leaf depths
leaf_depth = []
visited = set()
stack = [(0, 0)]

while stack:
    node, depth = stack.pop()
    if node in visited:
        continue
    visited.add(node)
    
    is_leaf = True
    for neighbor in graph[node]:
        if neighbor not in visited:
            is_leaf = False
            stack.append((neighbor, depth + 1))
    
    if is_leaf:
        leaf_depth.append(depth)

# Calculate MIN based on leaf depths
if len(graph[0]) == 1:
    MIN = 1 if all(d % 2 == 0 for d in leaf_depth) else 3
else:
    MIN = 1 if all(d % 2 == 0 for d in leaf_depth) or all(d % 2 == 1 for d in leaf_depth) else 3

print(MIN, MAX)