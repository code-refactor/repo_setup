#!/usr/bin/env python3

n, m = map(int, input().split())

dist = [0] * (n + 1)
for row in range(n + 1):
    dist[row] = [1] * (n + 1)

for i in range(m):
    a, b = map(int, input().split())
    dist[a][b] = dist[b][a] = 2

x, v, i = 3 - dist[1][n], [0] * (n + 1), 1
d = [n + 1] * (n + 1)
res =  d[1] = 0

while i != n:
    v[i] = 1
    for j in range(1, n + 1):
        if v[j] == 0 and dist[i][j] == x and d[j] > d[i] + 1:
            d[j] = d[i] + 1
    meu = n + 1

    for j in range(1, n + 1):
        if v[j] == 0 and d[j] < meu:
            meu = d[j]
            i = j

    if meu == n + 1:
        res = -1
        break

    elif i == n:
        res = d[n]
        break

print(res)
