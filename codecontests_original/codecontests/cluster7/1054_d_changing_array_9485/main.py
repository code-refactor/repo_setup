#!/usr/bin/env python3

n,k=list(map(int,input().split()))
arr=list(map(int,input().split()))
newarr=[0]

for num in arr:
  newarr+=[newarr[-1]^num]
dic={}
for num in newarr:
  x=(min(num,2**k-1-num),max(num,2**k-1-num))
  if x in dic:
    dic[x]+=1
  else:
    dic[x]=1
ans=0
for elem in dic:
  m=dic[elem]
  half=m//2
  ans+=half*(half-1)/2
  half=m-half
  ans+=half*(half-1)/2
ans=n*(n+1)/2-ans
print(int(ans))
  
    
