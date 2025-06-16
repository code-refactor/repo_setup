#!/usr/bin/env python3

import heapq
from collections import defaultdict


class Graph:
    def __init__(self, n):
        self.nodes = set(range(n))
        self.edges = defaultdict(list)
        self.distances = {}

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[from_node, to_node] = distance
        self.distances[to_node, from_node] = distance


def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}
    h = [(0, initial)]

    nodes = set(graph.nodes)

    while nodes and h:
        current_weight, min_node = heapq.heappop(h)
        try:
            while min_node not in nodes:
                current_weight, min_node = heapq.heappop(h)
        except IndexError:
            break

        nodes.remove(min_node)

        for v in graph.edges[min_node]:
            weight = current_weight + graph.distances[min_node, v]
            if v not in visited or weight < visited[v]:
                visited[v] = weight
                heapq.heappush(h, (weight, v))
                path[v] = min_node

    return visited, path


n, m, L, s, t = map(int, input().split())
min_g = Graph(n)
max_g = Graph(n)
g = Graph(n)
for _ in range(m):
    u, v, w = map(int, input().split())
    if w == 0:
        min_w = 1
        max_w = int(1e18)
    else:
        min_w = max_w = w
    min_g.add_edge(u, v, min_w)
    max_g.add_edge(u, v, max_w)
    g.add_edge(u, v, w)

min_ls, min_p = dijkstra(min_g, s)
try:
    min_l = min_ls[t]
    max_l = dijkstra(max_g, s)[0][t]
except KeyError:
    min_l = 0
    max_l = -1
if min_l <= L <= max_l:
    while min_l < L:
        a = s
        b = z = t
        while z != s:
            if g.distances[z, min_p[z]] == 0:
                max_g.distances[z, min_p[z]] = min_g.distances[z, min_p[z]]
                max_g.distances[min_p[z], z] = min_g.distances[z, min_p[z]]
                a = z
                b = min_p[z]
            z = min_p[z]
        new_dist = min_g.distances[a, b] + L - min_l
        max_g.distances[a, b] = new_dist
        max_g.distances[b, a] = new_dist

        min_g = max_g
        min_ls, min_p = dijkstra(min_g, s)
        min_l = min_ls[t]

    if min_l == L:
        print('YES')
        print('\n'.join('%s %s %s' % (u, v, w) for (u, v), w in min_g.distances.items() if u < v))
    else:
        print('NO')
else:
    print('NO')

