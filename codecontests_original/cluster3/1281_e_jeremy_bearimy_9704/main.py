#!/usr/bin/env python3

import sys

def input():
	return sys.stdin.readline().strip()

def solve():
	k = int(input())
	n = 2*k
	e = [[] for i in range(n)]
	p = [None]*(n)
	for i in range(n-1):
		a, b, t = map(int, input().split())
		a -= 1
		b -= 1
		e[a].append((b,t))
		e[b].append((a,t))
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
