#!/usr/bin/env python3

import sys
sys.setrecursionlimit(1000000)
def dfs(v, pr):
    global used
    global p
    global f
    if not f:
        return None
    if used[v]:
        f = False
    used[v] = True
    for i in range(len(p[v])):
        if p[v][i] != pr:
            dfs(p[v][i], v)
n, m = map(int, input().split())
p = []
for i in range(n):
    p.append([])
for i in range(m):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    p[a].append(b)
    p[b].append(a)
used = [False] * n
f = True
for i in range(n):
    if i != 0 and not used[i]:
        f = False
        break
    if not used[i]:
        dfs(i, -1)
if f:
    print('yes')
else:
    print('no')

        
