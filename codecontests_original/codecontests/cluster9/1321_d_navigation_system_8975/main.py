#!/usr/bin/env python3

import sys
from collections import deque
def bfs(g,src,d,found):
    q=deque()
    q.append(src)
    d[src]=0
    while q:
        rmv=q.popleft()
        for child in g[rmv]:
            if d[child]==-1:
                d[child]=d[rmv]+1
                q.append(child)
                found[child]=1
            elif d[child]==d[rmv]+1:
                found[child]+=1
                
            
        
n,m=map(int,sys.stdin.readline().split())
g=[]
gt=[]
for i in range(n):
    g.append(list())
    gt.append(list())
for _ in range(m):
    u,v=map(int,sys.stdin.readline().split())
    u-=1 
    v-=1
    g[u].append(v)
    gt[v].append(u)
k=int(sys.stdin.readline())
p=list(map(int,sys.stdin.readline().split()))
for i in range(len(p)):
    p[i]-=1
d=[-1]*(n)
found={}
bfs(gt,p[-1],d,found)
#print(d)
mn=0
mx=0
for i in range(1,k):
    if d[p[i-1]]-1!=d[p[i]]:
        mn+=1
        mx+=1
    elif found.get(p[i-1])!=None and found[p[i-1]]>1:
        mx+=1
print(mn,mx)
