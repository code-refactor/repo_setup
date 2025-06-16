#!/usr/bin/env python3

import sys
import io, os
input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
import collections
from collections import defaultdict
n=int(input())
c,root=[],0
graph=defaultdict(list)
for i in range(n):
    a,b=map(int,input().split())
    if a!=0:
        graph[i+1].append(a)
        graph[a].append(i+1)
    else:
        root=i+1
    c.append(b)
ans=[0]*(n+1)
store=[[] for _ in range(n+1)]
OBSERVE = 0
CHECK = 1
stack = [(OBSERVE, root, 0)]
if n==1 and c[0]==0:
    sys.stdout.write('YES'+'\n')
    sys.stdout.write('1'+'\n')
else:
    while len(stack):
        state, vertex, parent = stack.pop()
        if state == OBSERVE:
            stack.append((CHECK, vertex, parent))
            for child in graph[vertex]:
                if child != parent:
                    stack.append((OBSERVE, child, vertex))
        else:
            i=0
            while i<(len(graph[vertex])):
                if graph[vertex][i] != parent:
                    if len(graph[graph[vertex][i]])==1 and graph[vertex][i]!=root:
                        store[graph[vertex][i]].append([i+1,graph[vertex][i]])
                    store[vertex]+=store[graph[vertex][i]]
                i+=1
            store[vertex].sort()
            ok=True
            if c[vertex-1]>len(store[vertex]):
                ok=False
                break
            else:
                if len(store[vertex])>0:
                    if c[vertex-1]!=0:
                        store[vertex].insert(c[vertex-1],[store[vertex][c[vertex-1]-1][0]+1,vertex])
                    else:
                       store[vertex].insert(c[vertex-1],[store[vertex][c[vertex-1]][0],vertex])
                for ijk in range(len(store[vertex])):
                    store[vertex][ijk][0]=ijk+1
    if ok==True:
        for ij in store[root]:
            ans[ij[1]]=ij[0]
        sys.stdout.write('YES'+'\n')
        ans=' '.join(map(str,ans[1:]))
        sys.stdout.write(ans+'\n')
    else:
        sys.stdout.write('NO'+'\n')
