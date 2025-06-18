#!/usr/bin/env python3

from library import setup_io, read_int

input = setup_io()

def process_test_case():
    n = read_int()
    
    # Initialize adjacency list and node properties
    adj = [[] for _ in range(n + 1)]
    degree = [0] * (n + 1)  # Degree of each node (number of children)
    degree[1] = 1  # Root has special handling
    parent = [0] * (n + 1)  # Parent of each node
    
    # Read edges
    for _ in range(n - 1):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # First BFS to set up tree structure (parents and degrees)
    queue = [1]  # Start from root
    subtree_info = [[] for _ in range(n + 1)]  # Store (depth, max_k) for each subtree
    leaves = []  # Store leaf nodes
    
    while queue:
        node = queue.pop()
        for child in adj[node]:
            if child != parent[node]:
                degree[node] += 1
                parent[child] = node
                queue.append(child)
        
        # If node is a leaf (no children)
        if degree[node] == 0:
            leaves.append(node)
    
    # Bottom-up processing from leaves to root
    while leaves:
        node = leaves.pop()
        parent_node = parent[node]
        
        # If this is a leaf node with no subtree info
        if not subtree_info[node]:
            subtree_info[parent_node].append((1, 0))
        # If node has only one child
        elif len(subtree_info[node]) == 1:
            d, k = subtree_info[node][0]
            subtree_info[parent_node].append((d + 1, k))
        # If node has multiple children
        else:
            # Find minimum depth among children
            d = min(p[0] for p in subtree_info[node]) + 1
            # Find maximum k value among children or the maximum depth + 1
            k = max(max(p[1] for p in subtree_info[node]), 
                    max(p[0] for p in subtree_info[node]) + 1)
            subtree_info[parent_node].append((d, k))
        
        # Decrement degree of parent and check if it's ready to process
        degree[parent_node] -= 1
        if degree[parent_node] == 0:
            leaves.append(parent_node)
    
    # Calculate final answer for root node
    root = 1
    if len(subtree_info[root]) == 1:
        # If root has only one child, answer is the maximum of depth and k
        print(max(subtree_info[root][0]))
    else:
        # If root has multiple children
        k = max(p[1] for p in subtree_info[root])  # Maximum k value
        depths = [p[0] for p in subtree_info[root]]  # All depths
        max_depth = max(depths)
        depths.remove(max_depth)
        second_max_depth = max(depths) if depths else 0
        
        # Answer is the maximum of:
        # 1. Second largest depth + 1 (to move between subtrees)
        # 2. Largest depth
        # 3. Maximum k value from subtrees
        print(max(second_max_depth + 1, max_depth, k))

# Process all test cases
for _ in range(read_int()):
    process_test_case()