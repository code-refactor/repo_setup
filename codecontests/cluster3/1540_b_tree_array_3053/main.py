#!/usr/bin/env python3

from library import setup_io, read_int
from collections import deque

input = setup_io()

# Constants
MOD = 10**9 + 7

# Read input
n = read_int()
edges = []
for _ in range(n - 1):
    x, y = map(int, input().split())
    x -= 1  # Convert to 0-indexed
    y -= 1
    edges.append((x, y))

# Precompute path combinations
# PA[i][j] = number of paths of length j in a tree of size i
path_combinations = [[1]]  # PA[0][0] = 1
for i in range(n + 2):
    new_row = [0] * (i + 2)
    prev_row = path_combinations[-1]
    
    # Calculate combinations
    for j, val in enumerate(prev_row):
        new_row[j] = (new_row[j] + val) % MOD
        new_row[j + 1] = (new_row[j + 1] + val) % MOD
    
    path_combinations.append(new_row)
    
# Calculate prefix sums for each row
for row in path_combinations:
    for i in range(len(row) - 1):
        row[i + 1] = (row[i + 1] + row[i]) % MOD

# Precompute powers of 1/2
inv_2 = (MOD + 1) >> 1  # Modular inverse of 2
powers_of_half = [1]
for _ in range(n + 5):
    powers_of_half.append((powers_of_half[-1] * inv_2) % MOD)

# Modular inverse of n
inv_n = pow(n, MOD - 2, MOD)

# Calculate expected inversions
answer = 0
for start_node in range(n):
    # Build adjacency list for current root
    adj = [[] for _ in range(n)]
    for x, y in edges:
        adj[x].append(y)
        adj[y].append(x)
    
    # BFS to get tree structure from current root
    parent = [-1] * n
    queue = deque([start_node])
    processing_order = []
    depth = [0] * n
    
    while queue:
        node = queue.popleft()
        processing_order.append(node)
        
        for neighbor in adj[node]:
            if neighbor != parent[node]:
                parent[neighbor] = node
                adj[neighbor].remove(node)  # Remove parent from adjacency list
                queue.append(neighbor)
                depth[neighbor] = depth[node] + 1
    
    # Calculate subtree sizes
    subtree_size = [1] * n
    for node in reversed(processing_order[1:]):  # Skip root
        subtree_size[parent[node]] += subtree_size[node]
    
    # Calculate inversions for each node
    for node in processing_order:
        if node <= start_node:
            continue  # Skip nodes with smaller indices (not inversions)
        
        # Add direct contribution
        d = depth[node]
        answer = (answer + subtree_size[node] * inv_n) % MOD
        
        # Process path from node to root
        current = node
        while parent[current] != start_node:
            p = parent[current]
            siblings_size = subtree_size[p] - subtree_size[current]
            
            # Add contribution from this level
            contribution = (siblings_size * path_combinations[d-1][depth[p]-1]) % MOD
            contribution = (contribution * inv_n) % MOD
            contribution = (contribution * powers_of_half[d-1]) % MOD
            
            answer = (answer + contribution) % MOD
            current = p

print(answer)