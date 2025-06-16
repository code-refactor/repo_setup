#!/usr/bin/env python3

import sys
from collections import deque
 
 
reader = (line.rstrip() for line in sys.stdin)
input = reader.__next__
 
# v(G), e(G), special v
n, m, k = map(int, input().split())
a = list(map(int, input().split()))
 
# adjacency lists
g = [[] for _ in range(n + 1)] 
for _ in range(m):
    v, to = map(int, input().split())
    g[v].append(to)
    g[to].append(v)
 
dist_1 = [float('inf')] * (n + 1)
s = 1  # start vertex
dist_1[s] = 0
queue = deque([s])
while queue:
    v = queue.pop()
    for to in g[v]:
        if dist_1[to] > dist_1[v] + 1:
            dist_1[to] = dist_1[v] + 1
            queue.appendleft(to)
 
dist_n = [float('inf')] * (n + 1)
s = n  # start vertex
dist_n[s] = 0
queue = deque([s])
while queue:
    v = queue.pop()
    for to in g[v]:
        if dist_n[to] > dist_n[v] + 1:
            dist_n[to] = dist_n[v] + 1
            queue.appendleft(to)
            
 
a.sort(key=dist_1.__getitem__)
# print(dist_1)
# print(a)
# print(dist_n)
 
class SegmTree():
    def __init__(self, size):
        N = 1
        while N < size:
            N <<= 1
        self.N = N
        self.tree = [-float('inf')] * (2*self.N)
 
    def modify(self, i, value):
        i += self.N
        self.tree[i] = value
        while i > 1:
            self.tree[i>>1] = max(self.tree[i], self.tree[i^1])
            i >>= 1
 
    def query_range(self, l, r):
        l += self.N
        r += self.N
        result = -float('inf')
        while l < r:
            if l & 1:
                result = max(result, self.tree[l])
                l += 1
            if r & 1:
                r -= 1
                result = max(result, self.tree[r])
            l >>= 1
            r >>= 1
        return result
 
st = SegmTree(n + 1)
for v in a:
    st.modify(v, dist_n[v])
longestPossible = 0
for v in a:
    st.modify(v, -float('inf'))
    dist = dist_1[v] + 1 + st.query_range(0, n + 1)
    longestPossible = max(longestPossible, dist)
shortDist = min(dist_1[n], longestPossible)
 
print(shortDist)
