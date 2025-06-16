#!/usr/bin/env python3

from library import TreeBuilder, Utils

Utils.set_recursion_limit()
input = Utils.fast_io()

n = int(input())
a = list(map(int, input().split()))

edges = []
for _ in range(n-1):
    u, v, w = map(int, input().split())
    edges.append((u, v, w))

adj = TreeBuilder.from_edges(n, edges, indexed=1, weighted=True)
best = [0] * n
ans = 0

def dfs(u):
    stack = [(u, -1)]
    visit = [False] * n
    
    while stack:
        u, par = stack[-1]
        if not visit[u]:
            visit[u] = True
            for v, w in adj[u]:
                if v != par:
                    stack.append((v, u))
        else:
            cand = []
            for v, w in adj[u]:
                if v != par:
                    cand.append(best[v] + a[v] - w)
            cand.sort(reverse=True)
            cur = a[u]
            for i in range(2):
                if i < len(cand) and cand[i] > 0:
                    cur += cand[i]
            global ans
            ans = max(ans, cur)
            best[u] = cand[0] if len(cand) > 0 and cand[0] > 0 else 0
            stack.pop()

dfs(0)
print(ans)