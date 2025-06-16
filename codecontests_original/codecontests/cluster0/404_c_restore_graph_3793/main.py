#!/usr/bin/env python3

from sys import exit


n, k = map(int, input().split())
nodes = [[] for _ in range(n+1)]
edges = []

for node, dist in enumerate(map(int, input().split())):
    nodes[dist].append(node)

if len(nodes[0]) != 1 or len(nodes[1]) > k:
    print(-1)
else:
    for i in range(1, n):
        if len(nodes[i])*(k-1) < len(nodes[i+1]):
            print(-1)
            exit(0)
    for i in range(n):

        next = 0

        if len(nodes[i+1]) > 0:
            for j, node in enumerate(nodes[i]):

                current = 0

                while current < (k if i == 0 else k-1) and next < len(nodes[i+1]):
                    edges.append((node+1, nodes[i+1][next]+1))
                    next += 1
                    current += 1

    print(len(edges))
    print('\n'.join(map(lambda x: ' '.join([str(x[0]), str(x[1])]), edges)))
