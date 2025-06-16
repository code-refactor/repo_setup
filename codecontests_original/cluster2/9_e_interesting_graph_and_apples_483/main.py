#!/usr/bin/env python3

def dfs(v, comp):
    used[v] = comp
    for u in graph[v]:
        if not used[u]:
            dfs(u, comp)


n, m = map(int, input().split())
graph = [[] for i in range(n)]
for i in range(m):
    v, u = map(int, input().split())
    graph[v - 1].append(u - 1)
    graph[u - 1].append(v - 1)
used = [0] * n
ncomp = 0
for v in range(n):
    if not used[v]:
        ncomp += 1
        dfs(v, ncomp)
maxpwr = max(map(len, graph))
if n - m != ncomp or maxpwr > 2:
    if n == m and ncomp == 1 and maxpwr == 2:
        print("YES")
        print(0)
    else:
        print("NO")
else:
    print("YES")
    print(n - m)    
    leaves = []
    for v in range(n):
        if len(graph[v]) == 1:
            leaves.append([v + 1, used[v]])
        elif len(graph[v]) == 0:
            leaves.append([v + 1, used[v]])
            leaves.append([v + 1, used[v]])
    sets = []
    for i in range(len(leaves)):
        if leaves[i][0] == 0:
            continue
        for j in range(i + 1, len(leaves)):
            if leaves[j][0] == 0:
                continue            
            if leaves[i][1] == leaves[j][1]:
                continue
            seti = -1
            for k in range(len(sets)):
                if leaves[i][1] in sets[k]:
                    seti = k
                    break
            setj = -2
            for k in range(len(sets)):
                if leaves[j][1] in sets[k]:
                    setj = k
                    break
            if seti != setj:
                print(leaves[i][0], leaves[j][0])
                if seti >= 0:
                    if setj >= 0:
                        sets[seti] |= sets[setj]
                        sets.pop(setj)
                    else:
                        sets[seti].add(leaves[j][1])
                else:
                    if setj >= 0:
                        sets[setj].add(leaves[i][1])   
                    else:
                        sets.append(set([leaves[i][1], leaves[j][1]]))
                leaves[i][0] = 0
                leaves[j][0] = 0
                break
    for i in range(len(leaves)):
        if leaves[i][0] == 0:
            continue
        for j in range(i + 1, len(leaves)):
            if leaves[j][0] == 0:
                continue            
            print(leaves[i][0], leaves[j][0])
            break
        else:
            continue
        break