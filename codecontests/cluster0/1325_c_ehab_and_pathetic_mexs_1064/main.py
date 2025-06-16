from library import *

n = int_inp()
occ = [0] * n
graph = []

for i in range(n-1):
    x, y = ints()
    occ[x-1] += 1
    occ[y-1] += 1
    graph.append([x-1, y-1])
    
fin = [-1] * (n-1)
for i in range(n):
    if occ[i] >= 3:
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