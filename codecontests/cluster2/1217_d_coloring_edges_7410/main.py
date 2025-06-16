#!/usr/bin/env python3

import sys
input = sys.stdin.readline
def dfs(cur_node, childs, vis, cur_dfs):
    if cur_node in cur_dfs:
        return True

    if vis[cur_node]:
        return False

    vis[cur_node] = True
    cur_dfs.add(cur_node)
    for ele in childs[cur_node]:
        if dfs(ele, childs, vis, cur_dfs):
            return True

    cur_dfs.remove(cur_node)
    return False

n, m = map(int, input().split())
childs = [[] for i in range(n+1)]
has_dad = [False] * (n+1)
vis = [False] * (n+1)
ans2 = []
for i in range(m):
    x1, x2 = map(int, input().split())
    ans2.append(str((x1 < x2) + 1))
    childs[x1].append(x2)
    has_dad[x2] = True

has_cycle = False
for i in range(1, n+1):
    if not has_dad[i] and dfs(i, childs, vis, set()):
        has_cycle = True
        break

for i in range(1, n+1):
    if has_dad[i] and not vis[i]:
        has_cycle = True
        break

if has_cycle:
    print(2)
    print(' '.join(ans2))
else:
    print(1)
    print(' '.join(['1']*m))
