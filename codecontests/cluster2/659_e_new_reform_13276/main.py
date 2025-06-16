#!/usr/bin/env python3

import sys
from math import sqrt, gcd, ceil, log
# from bisect import bisect, bisect_left
from collections import defaultdict, Counter, deque
# from heapq import heapify, heappush, heappop
input = sys.stdin.readline
read = lambda: list(map(int, input().strip().split()))

sys.setrecursionlimit(200000)


def main(): 
	n, m = read()
	adj = defaultdict(list)
	visited = defaultdict(int)
	# visited
	for i in range(m):
		x, y = read()
		adj[x].append(y)
		adj[y].append(x)

	def dfs(ver):
		parent = defaultdict(int)
		stk = [(ver,0)]
		visited[ver] = 1
		parent[ver] = 0
		while stk:
			node, par = stk.pop()
			for child in adj[node]:
				if child == par:continue
				elif not visited[child]:
					visited[child] = 1
					parent[child] = node
					stk.append((child, node))
				elif parent[child] != node:
					return(0)
		return(1)

	ans = 0
	for i in range(1, n+1):
		if not visited[i]:
			ans += dfs(i)
			# print(i, visited)
	print(ans)
		# 




			






if __name__ == "__main__":
	main()