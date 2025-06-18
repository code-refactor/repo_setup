#!/usr/bin/env python3

import collections
tests = int(input())


def bfs(start, edges):
    q = collections.deque([start])
    dist = [-1]*(n+1)
    dist[start] = 0
    while(len(q) > 0):
        curr_node = q.popleft()
        for idx, neighbour in enumerate(edges[curr_node]):
            if dist[neighbour] == -1:
                q.append(neighbour)
                dist[neighbour] = dist[curr_node] + 1
    return dist

for t in range(tests):
    (n,m,a,b,c) = map(int, input().split(" "))
    costs = map(int, input().split(" "))
    costs = sorted(costs)
    edges = [[] for i in range(n+1)]
    partial_sums = [0]
    for nod, cost in enumerate(costs):
        costs[nod] = cost
        partial_sums.append(partial_sums[nod] + cost)
    for edge in range(m):
        (u,v) = map(int, input().split(" "))
        edges[u].append(v)
        edges[v].append(u)

    dist = [[],[],[]]
    dist[0] = bfs(a,edges)
    dist[1] = bfs(b,edges)
    dist[2] = bfs(c,edges)
    min_sum = 1<<62
    for i in range(1,n+1,1):
        if dist[0][i]+dist[1][i]+dist[2][i] > m: continue
        min_sum = min(min_sum, partial_sums[dist[1][i]] + partial_sums[dist[0][i]+dist[1][i]+dist[2][i]])
    print(min_sum)



