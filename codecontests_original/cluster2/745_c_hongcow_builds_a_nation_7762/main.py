#!/usr/bin/env python3

from collections import deque
n,m,k = map(int,input().split())
line = input().split()
gov = []
for i in range(k):
    gov.append(int(line[i])-1)
graph = {}
for i in range(m):
    u,v = map(int,input().split())
    u -= 1
    v -= 1
    if u not in graph:
        graph[u] = set()
    if v not in graph:
        graph[v] = set()
    graph[u].add(v)
    graph[v].add(u)
govgraph = {}
nottaken = set()
for i in range(n):
    nottaken.add(i)
for x in gov:
    nottaken.remove(x)
    if x in graph:
        d = deque()
        reach = set([x])
        d.append(x)
        while len(d) > 0:
            c = d.popleft()
            for i in graph[c]:
                if i not in reach:
                    reach.add(i)
                    nottaken.remove(i)
                    d.append(i)
        govgraph[x] = reach
    else:
        govgraph[x] = set([x])
ar = []
for c in govgraph:
    ar.append(govgraph[c])
ar.sort(key = lambda x: len(x), reverse=True)
meh = len(ar[0]) + len(nottaken)
ans = int((meh*(meh-1))/2)
for i in range(1,len(ar)):
    ans += int((len(ar[i])*(len(ar[i])-1))/2)
print(ans - m)
