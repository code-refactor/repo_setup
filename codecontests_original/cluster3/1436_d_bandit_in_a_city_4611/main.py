#!/usr/bin/env python3

n = int(input())
parent = [0] + [x-1 for x in list(map(int, input().split()))]
citizen = list(map(int, input().split()))
 
sz = [1] * n
for i in range(1, n):
    sz[parent[i]] = 0
#print(sz) 
for i in range(n-1, 0, -1):
    citizen[parent[i]] += citizen[i]
    sz[parent[i]] += sz[i]
#print(citizen)
#print(sz)
ans = 0
for i in range(n):
    if citizen[i]%sz[i]==0:
        ans=max(ans,citizen[i]//sz[i])
    else:
        ans=max(ans,(citizen[i]//sz[i])+1)
    #ans = max(ans, (citizen[i]+sz[i]-1)//sz[i])
 
print(ans)