#!/usr/bin/env python3

import sys
from array import array  # noqa: F401


def input():
    return sys.stdin.buffer.readline().decode('utf-8')


n = int(input())
beaver = list(map(int, input().split()))
adj = [[] for _ in range(n)]
deg = [0] * n

for u, v in (map(int, input().split()) for _ in range(n - 1)):
    adj[u - 1].append(v - 1)
    adj[v - 1].append(u - 1)
    deg[u - 1] += 1
    deg[v - 1] += 1

start = int(input()) - 1
deg[start] += 1000000

if n == 1:
    print(0)
    exit()

dp = [0] * n
stack = [i for i in range(n) if i != start and deg[i] == 1]
while stack:
    v = stack.pop()
    deg[v] = 0
    child = []
    child_dp = []

    for dest in adj[v]:
        if deg[dest] == 0:
            child.append(dest)
            child_dp.append(dp[dest])

        else:
            deg[dest] -= 1
            if deg[dest] == 1:
                stack.append(dest)

    child_dp.sort(reverse=True)
    x = min(beaver[v] - 1, len(child))
    dp[v] = 1 + sum(child_dp[:x]) + x
    beaver[v] -= x + 1
    for c in child:
        x = min(beaver[v], beaver[c])
        beaver[v] -= x
        dp[v] += 2 * x


x = min(beaver[start], len(adj[start]))
child_dp = sorted((dp[v] for v in adj[start]), reverse=True)
ans = sum(child_dp[:x]) + x
beaver[start] -= x

for c in adj[start]:
    x = min(beaver[start], beaver[c])
    beaver[start] -= x
    ans += 2 * x

print(ans)
