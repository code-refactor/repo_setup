#!/usr/bin/env python3

# Fast IO (only use in integer input)

import os,io
input=io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

t = int(input())
for _ in range(t):
    n,m = map(int,input().split())
    connectionList = []
    for _ in range(n):
        connectionList.append([])
    for _ in range(m):
        u,v = map(int,input().split())
        connectionList[u-1].append(v-1)
        connectionList[v-1].append(u-1)
    DFSLevel = [-1] * n
    DFSParent = [-1] * n
    vertexStack = []
    vertexStack.append((0,1,-1)) # vertex depth and parent
    while vertexStack:
        vertex,depth,parent = vertexStack.pop()
        if DFSLevel[vertex] != -1:
            continue
        DFSLevel[vertex] = depth
        DFSParent[vertex] = parent
        for nextV in connectionList[vertex]:
            if DFSLevel[nextV] == -1:
                vertexStack.append((nextV,depth + 1,vertex))
    if max(DFSLevel) >= n//2 + n % 2:
        for i in range(n):
            if DFSLevel[i] >= (n//2 + n%2):
                break
        longPath = [str(i + 1)]
        while DFSParent[i] != -1:
            longPath.append(str(DFSParent[i] + 1))
            i = DFSParent[i]
        print("PATH")
        print(len(longPath))
        print(" ".join(longPath))
    else:
        levelWithVertex = list(enumerate(DFSLevel))
        levelWithVertex.sort(key = lambda x: x[1])
        i = 0
        pair = []
        while i < len(levelWithVertex) - 1:
            if levelWithVertex[i][1] == levelWithVertex[i + 1][1]:
                pair.append([levelWithVertex[i][0],levelWithVertex[i + 1][0]])
                i += 2
            else:
                i += 1
        print("PAIRING")
        print(len(pair))
        for elem in pair:
            print(str(elem[0] + 1)+" "+str(elem[1] + 1))

