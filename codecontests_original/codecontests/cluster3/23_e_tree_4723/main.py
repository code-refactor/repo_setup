#!/usr/bin/env python3

from fractions import Fraction
n = int(input())

adj = [list() for x in  range(n)]
H = [0] * n
F = [0] * n
FoH = [list() for x in range(n)]
sz = 0
order = [0] * n
pi = [-1] * n

def dfs(u, p = -1):
  global pi, order, sz
  pi[u] = p
  for v in adj[u]:
    if v != p:
      dfs(v, u)
  order[sz] = u
  sz += 1


T1 = [0] * n
T2 = [0] * n
T3 = [0] * n

def solve(u, p = -1):
  global H, F, FoH
  F[u] = 1
  for v in adj[u]:
    if v != p:
      F[u] *= H[v]
      FoH[u].append(Fraction(F[v], H[v]))
  ans = F[u]
  FoH[u].sort()
  FoH[u].reverse()
  pd = 1
  s = 0
  for x in FoH[u]:
    pd *= x
    s += 1
    ans = max(ans, int(pd * F[u]) * (s+1))
  for v in adj[u]:
    if v != p:
      pd = 1
      s = 0
      for x in FoH[v]:
        pd *= x
        s += 1
        ans = max(ans, int(pd * F[u] * F[v]) // H[v] * (s+2))
  #print(u+1, ':', FoH[u], ans)
  H[u] = ans

for i in range(1, n):
  u, v = [int(x) for x in input().split()]
  u -= 1
  v -= 1
  adj[u].append(v)
  adj[v].append(u)

dfs(0)
for x in order:
  solve(x, pi[x])
print(H[0])

