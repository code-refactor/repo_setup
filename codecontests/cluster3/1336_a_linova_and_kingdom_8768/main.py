#!/usr/bin/env python3

import sys
sys.path.append('/home/justinchiu_cohere_com/minicode/codecontests/cluster3')
from library import Utils, TreeBuilder
import threading

input = Utils.fast_io()
Utils.set_recursion_limit()
threading.stack_size(10**8)
threading.stack_size(10**8)
def dfs(x,a):
    global v,d,l,adj
    v[x]=1
    d[x]=a
    c=0
    for i in adj[x]:
        if not v[i]:
            c+=dfs(i,a+1)+1
    l[x]=c
    return(l[x])
def main():
    global v,d,l,adj
    n,k=map(int,input().split())
    v=[0]*(n+1)
    l=[0]*(n+1)
    d=[0]*(n+1)
    adj=[]
    for i in range(n+1):
        adj.append([])
    for i in range(n-1):
        x,y=map(int,input().split())
        adj[x].append(y)
        adj[y].append(x)
    dfs(1,0)
    l1=[]
    for i in range(1,n+1):
        l1.append(l[i]-d[i])
    l1.sort(reverse=True)
    print(sum(l1[:n-k]))
    
t=threading.Thread(target=main)
t.start()
t.join()
        
    
    
        
    
    
    
