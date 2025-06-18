#!/usr/bin/env python3

from queue import *

n=int(input())
parent={}
child={}
for i in range(1,n+1):
    parent[i]=0
    child[i]=[]
l=list(map(int,input().split()))
for i in range(2,n+1):
    parent[i]=l[i-2]
    child[l[i-2]].append(i)
l=list(map(int,input().split()))
color={}
for i in range(1,n+1):
    color[i]=l[i-1]
    
q=Queue()
q.put(1)
ans=0
while(not(q.empty())):
    e=q.get()
    c=0
    if(e==1):
        c=0
    else:
        c=color[parent[e]]
    if(c!=color[e]):
        ans+=1
    for i in child[e]:
        q.put(i)
        
print(ans)


    
    
    
    
