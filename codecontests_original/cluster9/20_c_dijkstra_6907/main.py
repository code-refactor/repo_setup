#!/usr/bin/env python3


from collections import defaultdict
from heapq import heappush, heapify, heappop

INF = 10 ** 18
class Graph:
	def __init__(self):
		self.adj_list = defaultdict(list)

	def add_edge(self, src, dest, cost):
		self.adj_list[src].append((dest, cost))
		self.adj_list[dest].append((src, cost))


def dijkstra(graph, src, dest, n):
	dist = [INF] * n
	vis = [False] * n
	dist[src] = 0
	min_queue = [(0, src)]
	heapify(min_queue)
	parent = [-1] * n

	while min_queue:
		d, u = heappop(min_queue)
		if vis[u]:
			continue
		vis[u] = True
		for v, d2 in graph.adj_list[u]:
			if d2 + d < dist[v]:
				dist[v] = d2 + d
				heappush(min_queue, (dist[v], v))
				parent[v] = u

	if dist[dest] == INF:
		return "-1"
	path = []
	curr = dest
	while curr != -1:
		path.append(curr + 1)
		curr = parent[curr]
	path.reverse()
	return " ".join(str(i) for i in path)


def main():
    graph = Graph()
    
    n, m = [int(i) for i in input().split()]
    for i in range(m):
        u, v, w = [int(j) for j in input().split()]
        u -= 1
        v -= 1
        graph.add_edge(u, v, w)

    print(dijkstra(graph, 0, n - 1, n))

if __name__ == '__main__':
    main()



