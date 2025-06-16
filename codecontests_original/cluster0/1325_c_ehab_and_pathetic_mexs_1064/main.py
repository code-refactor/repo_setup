#!/usr/bin/env python3

n = int(input())
occ = [0 for i in range(n)]
graph = [[0,0] for i in range(n-1)]
for i in range(n-1):
    x, y = map(int,input().split())
    occ[x-1]+=1
    occ[y-1]+=1
    graph[i][0] = x-1
    graph[i][1] = y-1
    
fin = [-1 for i in range(n-1)]
for i in range(n):
    if occ[i] >= 3 :
        var = 0
        for j in range(n-1):
            if graph[j][0] == i or graph[j][1] == i:
                fin[j] = var
                var += 1
        break
else:
    var = 0
    for i in range(n):
        if var > 1:
            break
        if occ[i] == 1:
            for j in range(n-1):
                if graph[j][0] == i or graph[j][1] == i:
                    fin[j] = var
                    var += 1
                    break
for i in fin:
    if n == 2:
        print(0)
        break
    if i == -1:
        print(var)
        var += 1
    else:
        print(i)