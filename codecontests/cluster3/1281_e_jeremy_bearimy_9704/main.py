#!/usr/bin/env python3

import sys
sys.path.append('/home/justinchiu_cohere_com/minicode/codecontests/cluster3')
from library import Utils, TreeBuilder

input = Utils.fast_io()

def solve():
	k = int(input())
	n = 2*k
	
	# Read weighted edges
	edges = []
	for i in range(n-1):
		a, b, t = map(int, input().split())
		edges.append((a, b, t))
	
	# Build 0-indexed adjacency list with weights
	e = TreeBuilder.from_edges(n, edges, indexed=1, weighted=True)
	
	p = [None]*(n)
	q = [0]
	qi = 0
	while qi < len(q):
		x = q[qi]
		qi += 1
		px = p[x]
		for v, w in e[x]:
			if v != px:
				q.append(v)
				p[v] = x
	d1 = [False] * n
	d2 = [0] * n
	m = 0
	M = 0
	for qi in range(len(q)-1,-1,-1):
		x = q[qi]
		px = p[x]
		cnt = 1
		c1 = 1
		for v, w in e[x]:
			if v != px:
				if d1[v]:
					m += w
					cnt += 1
				dv = d2[v]
				M += w * min(dv, n - dv)
				c1 += dv
		d1[x] = cnt % 2
		d2[x] = c1
	print(m, M)

for i in range(int(input())):
	solve()
