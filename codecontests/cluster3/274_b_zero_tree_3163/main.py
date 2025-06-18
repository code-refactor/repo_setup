#!/usr/bin/env python3

from library import read_int, read_ints

# Read input
n = read_int()
adj = [[] for _ in range(n + 1)]
adj[1] = [0]  # Add sentinel parent for root

# Build adjacency list
for _ in range(n - 1):
    a, b = map(int, input().split())
    adj[a].append(b)
    adj[b].append(a)

# Read node values
values = read_ints()

# Split positive and negative values
neg_ops, pos_ops = [0] * (n + 1), [0] * (n + 1)
for i, val in enumerate(values, 1):
    if val < 0:
        neg_ops[i] = -val
    else:
        pos_ops[i] = val

# Compute parent pointers via DFS
stack, parent = [1], [0] * (n + 1)
while stack:
    node = stack.pop()
    for neighbor in adj[node]:
        if parent[neighbor] == 0 and neighbor != 1:  # Skip visited nodes and root's parent
            parent[neighbor] = node
            stack.append(neighbor)

# Count children for each node
degree = [len(children) for children in adj]

# Process leaf nodes (bottom-up)
leaves = [node for node in range(2, n + 1) if degree[node] == 1]
max_neg, max_pos = [0] * (n + 1), [0] * (n + 1)

while leaves:
    node = leaves.pop()
    p = parent[node]
    
    # Update max operations needed for parent
    max_neg[p] = max(max_neg[p], neg_ops[node])
    max_pos[p] = max(max_pos[p], pos_ops[node])
    
    # Reduce parent's degree and check if it becomes a leaf
    degree[p] -= 1
    if degree[p] == 1:  # Parent becomes a leaf
        leaves.append(p)
        
        # Update operations needed for this node
        if neg_ops[p] > 0:  # Node needs negative operations
            if max_neg[p] - max_pos[p] > neg_ops[p]:
                neg_ops[p], pos_ops[p] = max_neg[p], max_neg[p] - neg_ops[p]
            else:
                neg_ops[p], pos_ops[p] = max_pos[p] + neg_ops[p], max_pos[p]
        else:  # Node needs positive operations
            if max_pos[p] - max_neg[p] > pos_ops[p]:
                neg_ops[p], pos_ops[p] = max_pos[p] - pos_ops[p], max_pos[p]
            else:
                neg_ops[p], pos_ops[p] = max_neg[p], max_neg[p] + pos_ops[p]

# Print total operations needed
print(neg_ops[1] + pos_ops[1])