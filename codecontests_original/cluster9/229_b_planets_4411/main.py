#!/usr/bin/env python3

from heapq import *

n, m = map(int, input().split())
l = []
from copy import *
from bisect import *
from math import *
from sys import *
for _ in range(0, n + 2):
    l.append([])
for i in range(0, m):
    a, b, c = map(int, stdin.readline().split())
    l[a].append((c, b))
    l[b].append((c, a))

dist = [10000000000]*(n+3)
def helper(lst, val):
    if lst[0] > val or lst[-1] < val:
        return val
    v = bisect_left(lst, val)
    if lst[v] != val:
        return val
    else:
        l = 1
        h = len(lst) - v
        # lst.append(232767324)
        #tq=int(log(h,2))
        z = 20000000000
        cp=0
        while l<h:
            m = (l + h) // 2

            if val + m == lst[v + m]:
                l = m+1
            else:
                h, z = m, m

        return (lst[len(lst)-1]+1-val if z==20000000000 else z) + val


def dij_modified(delay,t):
    vis = [0] * (n + 3)
    dist[1] = t
    h = []
    heappush(h, (t, 1))
    heapify(h)
    while h:
        val = heappop(h)
        if vis[val[1]] != 0:
            continue
        vis[val[1]] = 1
        x = val[1]
        if len(delay[x-1])>0 and x!=n:
            dist[x]= helper(delay[x-1],dist[x])


        for i in l[x]:
            d = i[0]
            e = i[1]
            if dist[x] + d < dist[e]:
                dist[e] = dist[x] + d
                heappush(h, (dist[e], e))
delay =[]
for i in range(0,n):
    tlst=map(int, stdin.readline().split())
    x = next(tlst)
    if(x):delay.append(list(tlst)[0:])
    else: delay.append([-1])
x=delay[0]
t=0
dij_modified(delay,t)
if dist[n]<10000000000:
    print (dist[n])
else:
    print (-1)

