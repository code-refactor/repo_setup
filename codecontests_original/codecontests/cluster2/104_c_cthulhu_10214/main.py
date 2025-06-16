#!/usr/bin/env python3

n, m = [int(i) for i in input().split()]
adj = [[] for i in range(n+1)]
seen = [False for i in range(n+1)]
pai = [0 for i in range(n+1)]
ciclos = 0

def dfs (u):
    seen[u] = True
    global ciclos
    for v in adj[u]:
        if not seen[v]:
            pai[v] = u
            dfs(v)
        elif v != pai[u]:
            ciclos += 1

for i in range(m):
    x, y = [int(i) for i in input().split()]
    adj[x].append(y)
    adj[y].append(x)

dfs(1)
conexo = True

for i in range(1, n+1, 1):
    if not seen[i]:
        conexo = False

if conexo and ciclos/2 == 1:
    print('FHTAGN!')
else:
    print('NO')
exit(0)
