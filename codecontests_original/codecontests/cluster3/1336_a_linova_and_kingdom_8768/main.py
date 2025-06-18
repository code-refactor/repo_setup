#!/usr/bin/env python3

import os
import sys
from io import BytesIO, IOBase
 
BUFSIZE = 8192
 
 
class FastIO(IOBase):
    newlines = 0
 
    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
 
    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()
 
    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()
 
    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)
 
 
class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")
 
 
sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")
##################################################
import threading
sys.setrecursionlimit(200000)
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
        
    
    
        
    
    
    
