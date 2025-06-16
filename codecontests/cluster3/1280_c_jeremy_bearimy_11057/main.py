#!/usr/bin/env python3

import sys
sys.path.append('/home/justinchiu_cohere_com/minicode/codecontests/cluster3')
from library import Utils, TreeBuilder

input = Utils.fast_io()

for T in range(int(input())):
    k = int(input())
    
    # Read weighted edges
    edges = []
    for _ in range(2 * k - 1):
        a, b, weight = map(int, input().split())
        edges.append((a, b, weight))
    
    # Build adjacency list with weights
    adjacencies = TreeBuilder.from_edges(2 * k + 1, edges, indexed=1, weighted=True)

    parents = [0] * (2 * k + 1)
    weights = [0] * (2 * k + 1)

    root = 1 # arbitrary
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

    subtree_sizes = [1] * (2 * k + 1)
    maximum = minimum = 0
    index = len(queue) - 1
    while index >= 0: # build up the tree
        node = queue[index]
        subtree_sizes[parents[node]] += subtree_sizes[node]
        if subtree_sizes[node] & 1:
            minimum += weights[node]
        maximum += weights[node] * min(subtree_sizes[node], 2 * k - subtree_sizes[node])
        index -= 1
    print(minimum, maximum)
