#!/usr/bin/env python3

import sys

input = sys.stdin.readline

def solve():
	n = int(input())
	g = [[] for i in range(n+1)]
	for i in range(1, n):
		u, v = map(int, input().split())
		g[u].append(v)
		g[v].append(u)
	q = [1]
	d = [None]*(n+1)
	d[1] = 0
	i = 0
	while i < len(q):
		x = q[i]
		#print(x)
		i += 1
		for v in g[x]:
			if d[v] is None:
				q.append(v)
				d[v] = d[x] + 1
				g[v].remove(x)
	m = [0]*(n+1)
	M = [0]*(n+1)
	cnt = 0
	for i in range(len(q)-1,-1,-1):
		x = q[i]
		if len(g[x]) == 0:
			m[x] = 1
			M[x] = 1
			cnt += 1
		elif d[x] % 2 == 0:
			c = 0
			C = int(1e9)
			for v in g[x]:
				c += m[v]
			for v in g[x]:
				C = min(C, M[v])
			m[x] = c
			M[x] = C
		else:
			c = int(1e9)
			C = 0
			for v in g[x]:
				c = min(c, m[v])
			for v in g[x]:
				C += M[v]
			m[x] = c
			M[x] = C
	print(cnt + 1 - M[x], m[1])

solve()
