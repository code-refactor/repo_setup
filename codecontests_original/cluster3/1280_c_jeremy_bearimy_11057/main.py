#!/usr/bin/env python3

import sys
input = sys.stdin.buffer.readline

for T in range(int(input())):
    k = int(input())
    counts = [0] * (2 * k + 1)
    adjacencies = [list() for i in range(2 * k + 1)]
    for _ in range(2 * k - 1):
        a, b, weight = map(int, input().split())
        counts[a] += 1; counts[b] += 1
        adjacencies[a].append((b, weight))
        adjacencies[b].append((a, weight))

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
