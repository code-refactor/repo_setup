#!/usr/bin/env python3

import sys
from sys import stdin

from collections import deque
def NC_Dij(lis,start):

    ret = [float("inf")] * len(lis)
    ret[start] = 0
    
    q = deque([start])
    plis = [i for i in range(len(lis))]

    while len(q) > 0:
        now = q.popleft()

        for nex in lis[now]:

            if ret[nex] > ret[now] + 1:
                ret[nex] = ret[now] + 1
                plis[nex] = now
                q.append(nex)

    return ret,plis

tt = int(stdin.readline())

for loop in range(tt):

    stdin.readline()
    n,m = map(int,stdin.readline().split())

    lis = [ [] for i in range(n) ]
    for i in range(m):
        u,v = map(int,stdin.readline().split())
        u -= 1
        v -= 1
        lis[u].append(v)

    dlis,tmp = NC_Dij(lis,0)

    dind = []
    for i in range(n):
        dind.append((dlis[i],i))
    dind.sort()
    dind.reverse()

    ans = [None] * n

    for nd,ind in dind:
        now = nd
        for nex in lis[ind]:
            if dlis[nex] > nd:
                now = min(now,ans[nex])
            else:
                now = min(now,dlis[nex])
        ans[ind] = now
    print (*ans)