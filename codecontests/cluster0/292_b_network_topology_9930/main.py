#!/usr/bin/env python3

n,m=map(int,input().split())
arr=[0]*(n+1)
for w in range(m):
    a,b=map(int,input().split())
    arr[a]+=1
    arr[b]+=1
c1=0
c2=0
cs=0
for i in range(1,n+1):
    if arr[i]==1:
        c1+=1
    if arr[i]==2:
        c2+=1
    if arr[i]==n-1:
        cs+=1
if c1==2 and c2==n-2:
    print("bus topology")
elif c2==n:
    print("ring topology")
elif c1==n-1 and cs==1:
    print("star topology")
else:
    print("unknown topology")