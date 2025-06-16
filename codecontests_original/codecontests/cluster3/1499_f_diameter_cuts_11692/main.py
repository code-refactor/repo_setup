#!/usr/bin/env python3

import sys
from collections import deque

input = lambda :sys.stdin.buffer.readline()
mi = lambda :map(int,input().split())
li = lambda :list(mi())

mod = 998244353

N,K = mi()
edge = [[] for i in range(N)]
for _ in range(N-1):
    a,b = mi()
    edge[a-1].append(b-1)
    edge[b-1].append(a-1)

parent = [-1 for i in range(N)]
deq = deque([0])
res = []
while deq:
    v = deq.popleft()
    res.append(v)
    for nv in edge[v]:
        if nv!=parent[v]:
            parent[nv] = v
            deq.append(nv)

dp = [[1] for i in range(N)]

def merge(v,nv):
    res_dp = [0 for i in range(max(len(dp[v]),len(dp[nv])+1))]

    for i in range(len(dp[v])):
        for j in range(len(dp[nv])):
            if j+1+i <= K:
                res_dp[max(j+1,i)] += dp[v][i] * dp[nv][j]
                res_dp[max(j+1,i)] %= mod
            res_dp[i] += dp[v][i] * dp[nv][j]
            res_dp[i] %= mod

    dp[v] = res_dp

for v in res[::-1]:
    for nv in edge[v]:
        if nv==parent[v]:
            continue
        merge(v,nv)

print(sum(dp[0][i] for i in range(min(K+1,len(dp[0])))) % mod)
