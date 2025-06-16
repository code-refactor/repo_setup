#!/usr/bin/env python3

import sys
sys.path.append('..')

input = lambda: sys.stdin.readline().rstrip()

from collections import deque
mod = 10 ** 9 + 7
N = int(input())
E = []
for _ in range(N - 1):
    x, y = map(int, input().split())
    x, y = x-1, y-1
    E.append((x, y))

pre = [1]
PA = [pre]
for i in range(N + 2):
    ne = [0] * (i + 2)
    for j, a in enumerate(pre):
        ne[j] = (ne[j] + a) % mod
        ne[j+1] = (ne[j+1] + a) % mod
    PA.append(ne)
    pre = ne
for pa in PA:
    for i in range(len(pa) - 1):
        pa[i+1] = (pa[i+1] + pa[i]) % mod

i2 = mod + 1 >> 1
poi2 = [1]
for _ in range(N + 5):
    poi2.append(poi2[-1] * i2 % mod)
iN = pow(N, mod - 2, mod)
ans = 0
for i0 in range(N):
    X = [[] for i in range(N)]
    for x, y in E:
        X[x].append(y)
        X[y].append(x)

    P = [-1] * N
    Q = deque([i0])
    R = []
    D = [0] * N
    while Q:
        i = deque.popleft(Q)
        R.append(i)
        for a in X[i]:
            if a != P[i]:
                P[a] = i
                X[a].remove(i)
                deque.append(Q, a)
                D[a] = D[i] + 1
    
    size = [1] * N
    for j in R[1:][::-1]:
        size[P[j]] += size[j]
    
    for j in R:
        if j <= i0: continue
        d = D[j]
        ans = (ans + size[j] * iN)
        k = j
        while P[k] != i0:
            p = P[k]
            s = size[p] - size[k]
            ans = (ans + s * PA[d-1][D[p]-1] % mod * iN % mod * poi2[d-1]) % mod
            k = p

print(ans)