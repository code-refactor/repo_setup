#!/usr/bin/env python3

import sys
import io, os
input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

n,m,k = map(int, input().split())
g = [[] for i in range(n)]
toid = {}
for i in range(m):
    x,y,w = map(int, input().split())
    x,y = x-1, y-1
    g[x].append((w,y))
    g[y].append((w,x))
    toid[(x,y)] = i
    toid[(y,x)] = i

if k == 0:
    print(0)
    exit()

import heapq
INF = 10**18
def dijkstra(s, edge):
    n = len(edge)
    dist = [INF]*n
    prev = [-1]*n
    dist[s] = 0
    edgelist = []
    heapq.heappush(edgelist,(dist[s], s))
    while edgelist:
        minedge = heapq.heappop(edgelist)
        if dist[minedge[1]] < minedge[0]:
            continue
        v = minedge[1]
        for e in edge[v]:
            if dist[e[1]] > dist[v]+e[0]:
                dist[e[1]] = dist[v]+e[0]
                prev[e[1]] = v
                heapq.heappush(edgelist,(dist[e[1]], e[1]))
    return dist, prev

dist, prev = dijkstra(0, g)
G = [[] for i in range(n)]
for i, p in enumerate(prev):
    if prev[i] != -1:
        G[p].append(i)
#print(G)
s = []
s.append(0)
order = []
while s:
    v = s.pop()
    order.append(v)
    for u in G[v]:
        s.append(u)
#print(order)
ans = []
for v in order:
    for u in G[v]:
        ans.append(toid[(v, u)]+1)
        if len(ans) == k:
            break
    else:
        continue
    break
print(len(ans))
print(*ans)
