#!/usr/bin/env python3

from queue import *

n = int(input())
g = [[] for x in range(n)]

for i in range(n-1):
  a, b = map(int, input().split())
  a -= 1
  b -= 1
  g[a].append(b)
  g[b].append(a)

used = [0]*n

anw = 0

def solve(v, d, r):
  global anw
  q = Queue()
  q.put((v, d, r))
  while not q.empty():
    v, d, r = q.get(v)
    used[v] = True
    for u in g[v]:
      if not used[u]:
        q.put((u, d+1, r*(len(g[v])-(v!=0))))
        #print("put", u)
    #print("so at", v, "len", len(g[v]))
    if v != 0 and len(g[v]) == 1:
      #print("At ", v, "is", d, r)
      anw += d/r
  
solve(0, 0, 1)
print(anw)