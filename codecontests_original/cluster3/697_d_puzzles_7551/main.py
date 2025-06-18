#!/usr/bin/env python3

import sys
input = sys.stdin.readline

n = int(input())
par = [-1] + [int(i) - 1 for i in input().split()]
child = [[] for i in range(n)]
for i in range(1, n):
    child[par[i]].append(i)

size = [1] * n
def dfs():
    stack = [0]
    visit = [False] * n
    while stack:
        u = stack[-1]
        if not visit[u]:
            for v in child[u]:
                stack.append(v)
            visit[u] = True
        else:
            for v in child[u]:
                size[u] += size[v]
            stack.pop()

ans = [0] * n
ans[0] = 1
def dfs2():
    stack = [0]
    while stack:
        u = stack.pop()
        sm = 0
        for v in child[u]:
            sm += size[v]
        for v in child[u]:
            ans[v] = (sm - size[v]) * 0.5 + 1 + ans[u]
            stack.append(v)

dfs()
dfs2()
print(*ans)


