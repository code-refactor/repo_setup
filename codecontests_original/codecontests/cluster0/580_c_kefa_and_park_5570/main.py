#!/usr/bin/env python3

M=lambda:map(int,input().split())
n,m=M()
*c,=M()
t=[[]for i in range(n)]
v=[0]*n
for i in range(n-1):
    x,y=M()
    t[x-1].append(y-1)
    t[y-1].append(x-1)
a=i=0
q=[(0,0)]
while i<len(q):
    x,N=q[i]
    v[x]=1
    if c[x]+N<=m:
        L=1
        for y in t[x]:
            if not v[y]:
                L=0
                q.append((y,c[x]*(c[x]+N)))
        if L:
            a+=1
    i+=1
print(a)
