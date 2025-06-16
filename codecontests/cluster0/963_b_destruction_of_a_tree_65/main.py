#!/usr/bin/env python3

from collections import defaultdict,deque
import sys
import bisect
import math
input=sys.stdin.readline
mod=1000000007

def bfs(root,count):
    q=deque([root])
    vis.add(root)
    while q:
        vertex=q.popleft()
        for child in graph[vertex]:
            if ans[child]==0:
                ans[child]=count+1
                count+=1
            if child not in vis:
                q.append(child)
                vis.add(child)
                
graph=defaultdict(list)
n=int(input())
p=[int(i) for i in input().split() if i!='\n']
if n&1:
    for i in range(n):
        if p[i]!=0:
            graph[p[i]].append(i+1)
            graph[i+1].append(p[i])
    length=[0]*(n+1)
    for i in graph:
        length[i]=len(graph[i])
    CHECK,OBSERVE=1,0
    stack=[(OBSERVE,1,0)]
    ans=[0]*(n+1)
    count=0
    while stack:
        state,vertex,parent=stack.pop()
        if state==OBSERVE:
            stack.append((CHECK,vertex,parent))
            for child in graph[vertex]:
                if child != parent:
                    stack.append((OBSERVE,child,vertex))
        else:
            if length[vertex]%2==0:
                count+=1
                ans[vertex]=count
                length[parent]-=1
    vis=set()
    bfs(1,count)
    out=[0]*(n)
    for i in range(1,n+1):
        out[ans[i]-1]=i
    print('YES')
    for i in out:
        sys.stdout.write(str(i)+'\n')
else:
    print('NO')
        
    
            
        
        
        
    
    
