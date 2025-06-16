#!/usr/bin/env python3

from collections import defaultdict
l=lambda :map(int,input().split())
n,m=l()
c=list(l())
graph=defaultdict(set)
for i in range(m):
    a,b=l()
    if c[a-1]==c[b-1]:
        continue
    graph[c[a-1]].add(c[b-1])
    graph[c[b - 1]].add(c[a - 1])
d,f=min(c),0
for i in sorted(graph):
    h=len(graph[i])
    if h>f:
        f=h
        d=i
print(d)