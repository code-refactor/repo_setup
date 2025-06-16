#!/usr/bin/env python3

import sys
readline = sys.stdin.readline

def parorder(Edge, p):
    N = len(Edge)
    par = [0]*N
    par[p] = -1
    stack = [p]
    order = []
    visited = set([p])
    ast = stack.append
    apo = order.append
    while stack:
        vn = stack.pop()
        apo(vn)
        for vf in Edge[vn]:
            if vf in visited:
                continue
            visited.add(vf)
            par[vf] = vn
            ast(vf)
    return par, order

def getcld(p):
    res = [[] for _ in range(len(p))]
    for i, v in enumerate(p[1:], 1):
        res[v].append(i)
    return res


N = int(readline())
MOD = 998244353
Edge = [[] for _ in range(N)]
for _ in range(N-1):
    a, b = map(int, readline().split())
    a -= 1
    b -= 1
    Edge[a].append(b)
    Edge[b].append(a)

P, L = parorder(Edge, 0)
C = getcld(P)

dp = [[1, 1, 0, 0, 1] for _ in range(N)]
for p in L[::-1]:
    if not C[p]:
        continue
    res = 1
    res2 = 1
    res3 = 1
    for ci in C[p]:
        res = (res*(dp[ci][2] + dp[ci][3] + dp[ci][4])) % MOD
        res2 = (res2*(dp[ci][1] + dp[ci][2] + 2*dp[ci][3] + dp[ci][4])) % MOD
        res3 = (res3*(sum(dp[ci]) + dp[ci][2] + dp[ci][3])) % MOD
    dp[p][0] = res
    dp[p][1] = res
    dp[p][2] = (res2 - res)%MOD
    dp[p][3] = (res3 - res)%MOD
    dp[p][4] = res
print((dp[0][2] + dp[0][3] + dp[0][4] - 1) %MOD)