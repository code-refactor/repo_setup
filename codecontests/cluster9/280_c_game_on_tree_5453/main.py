#!/usr/bin/env python3

# https://codeforces.com/problemset/problem/280/C
from collections import defaultdict, deque
import sys

nodes = int(sys.stdin.readline())
edges = defaultdict(list)
for line in sys.stdin:
    a, b = line.split()
    a = int(a)
    b = int(b)
    edges[a].append(b)
    edges[b].append(a)
bfs = deque([(1, 1)])
depths = {}
while bfs:
    nid, depth = bfs.popleft()
    if nid in depths:
        continue
    depths[nid] = depth
    for n2 in edges[nid]:
        bfs.append((n2, depth + 1))
print(sum(1.0 / d for d in sorted(depths.values(), reverse=True)))