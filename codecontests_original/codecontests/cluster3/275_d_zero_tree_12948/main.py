#!/usr/bin/env python3

import sys

def minp():
	return sys.stdin.readline().strip()

n = int(minp())
e = [0]
p = [None]*(n+1)
for i in range(n):
	e.append([])
for i in range(n-1):
	a, b = map(int,minp().split())
	e[a].append(b)
	e[b].append(a)
v = list(map(int,minp().split()))
plus = [0]*(n+1)
minus = [0]*(n+1)

was = [False]*(n+1)
was[1] = True
i = 0
j = 1
q = [0]*(n+100)
q[0] = 1
p[1] = 0
while i < j:
	x = q[i]
	i += 1
	for y in e[x]:
		if not was[y]:
			was[y] = True
			p[y] = x
			q[j] = y
			j += 1

i = j-1
while i >= 0:
	x = q[i]
	i -= 1
	s = minus[x] - plus[x]
	z = v[x-1] + s
	pp = p[x]
	#print(x, p[x], plus[x], minus[x], '-', s[x], v[x-1]+s[x], v[0]+s[1])
	#print(-(plus[x]-minus[x]),s[x])
	minus[pp] = max(minus[x],minus[pp])
	plus[pp] = max(plus[x],plus[pp])
	if z > 0:
		plus[pp] = max(plus[pp],plus[x]+z)
	elif z < 0:
		minus[pp] = max(minus[pp],minus[x]-z)
#print(v[0])
#print(plus[0], minus[0])
print(plus[0] + minus[0])