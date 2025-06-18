#!/usr/bin/env python3

from library import setup_io, read_int

input = setup_io()

for T in range(read_int()):
    k = read_int()
    counts = [0] * (2 * k + 1)
    adjacencies = [list() for i in range(2 * k + 1)]
    
    # Read edges
    for _ in range(2 * k - 1):
        a, b, weight = map(int, input().split())
        counts[a] += 1
        counts[b] += 1
        adjacencies[a].append((b, weight))
        adjacencies[b].append((a, weight))

    # BFS to create tree
    parents = [0] * (2 * k + 1)
    weights = [0] * (2 * k + 1)
    
    root = 1  # Arbitrary root
    parents[root] = root
    queue = [0] * (2 * k)
    head, tail = 0, 0
    queue[tail] = root
    tail += 1
    
    while head < tail:
        node = queue[head]
        for child, weight in adjacencies[node]:
            if parents[child] < 1:
                parents[child] = node
                weights[child] = weight
                queue[tail] = child
                tail += 1
        head += 1

    # Calculate answer with tree traversal
    subtree_sizes = [1] * (2 * k + 1)
    maximum = minimum = 0
    index = len(queue) - 1
    
    while index >= 0:  # Build up the tree from leaves to root
        node = queue[index]
        subtree_sizes[parents[node]] += subtree_sizes[node]
        
        # Calculate minimum
        if subtree_sizes[node] & 1:  # If subtree size is odd
            minimum += weights[node]
        
        # Calculate maximum
        maximum += weights[node] * min(subtree_sizes[node], 2 * k - subtree_sizes[node])
        
        index -= 1
    
    print(minimum, maximum)