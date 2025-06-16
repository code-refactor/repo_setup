#!/usr/bin/env python3

n = int(input())
g = []
for i in range(n):
    t = input().split()
    g.append([ int(t[0]), int(t[1]), False ])

def visita(i):
    g[i][2] = True
    for j in range(n):
        if g[j][2] == False and (g[i][0] == g[j][0] or g[i][1] == g[j][1]):
            visita(j)

cnt = -1
for i in range(n):
    if g[i][2] == False:
        cnt += 1
        visita(i)

print(cnt)