#!/usr/bin/env python3

import sys
from sys import stdin
from collections import deque

n,k = map(int,stdin.readline().split())
N,K = n,k

lis = [ [] for i in range(N) ]
for i in range(N-1):
    x,y = map(int,stdin.readline().split())
    x -= 1
    y -= 1

    lis[x].append(y)
    lis[y].append(x)

a = list(map(int,stdin.readline().split()))

#bfs
p = [i for i in range(N)]
vlis = []
q = deque([0])
while q:
    v = q.popleft()
    vlis.append(v)

    for nex in lis[v]:
        if nex != p[v]:
            p[nex] = v
            q.append(nex)

#dp-first
dp = [[0] * (2*k) for i in range(N)]
for ind in range(N-1,-1,-1):
    v = vlis[ind]
    dp[v][0] ^= a[v]

    for nex in lis[v]:
        if nex != p[v]:
            for nk in range(2*k):
                dp[v][(nk+1) % (2*k)] ^= dp[nex][nk]

#dp2
ans = [None] * N
for v in vlis:

    if v == 0:
        now = 0
        for i in range(k,2*k):
            now ^= dp[v][i]
        ans[v] = min(now,1)

    else:
        pcopy = [dp[p[v]][i] for i in range(2*k)]
        for i in range(2*k):
            pcopy[(i+1) % (2*k)] ^= dp[v][i]
        for i in range(2*k):
            dp[v][(i+1) % (2*k)] ^= pcopy[i]

        now = 0
        for i in range(k,2*k):
            now ^= dp[v][i]
        ans[v] = min(now,1)

print (*ans)