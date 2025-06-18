#!/usr/bin/env python3

import collections as cc
import sys
input=sys.stdin.readline
#sys.setrecursionlimit(10**9)
I=lambda:list(map(int,input().split()))
n,m=I()
g=[set() for i in range(n+1)]
xx=[0]*(n+1)
for i in range(m):
	x,y=I()
	g[x].add(y)
	g[y].add(x)
parent=[i for i in range(n+1)]
def find(x):
	while x!=parent[x]:
		x=parent[x]
	return x
def union(x,y):
	a=find(x)
	b=find(y)
	if a!=b:
		parent[a]=parent[b]=min(a,b)
ff=cc.defaultdict(int)
used=cc.defaultdict(int)
for i in range(1,n+1):
	if find(i)==i:
			
		for j in range(1,n+1):
			if j not in g[i]:
				g[i]&=g[j]
		for j in range(1,n+1):
			if j not in g[i]:
				union(i,j)
				
 
print(len(set([find(i) for i in range(1,n+1)]))-1)