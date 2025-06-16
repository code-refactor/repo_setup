#!/usr/bin/env python3

import sys
input = lambda: sys.stdin.readline().rstrip()

def scc(E):
    n = len(E)
    iE = [[] for _ in range(n)]
    for i, e in enumerate(E):
        for v in e:
            iE[v].append(i)
    T = []
    done = [0] * n # 0 -> 1 -> 2
    ct = 0
    for i0 in range(n):
        if done[i0]: continue
        Q = [~i0, i0]
        while Q:
            i = Q.pop()
            if i < 0:
                if done[~i] == 2: continue
                done[~i] = 2
                T.append(~i)
                ct += 1
                continue
            if i >= 0:
                if done[i]: continue
                done[i] = 1
            for j in E[i]:
                if done[j]: continue
                Q.append(~j)
                Q.append(j)
    
    done = [0] * n
    SCC = []
    ### ID ���K�v�ȂƂ�
    I = [0] * n
    ###
    for i0 in T[::-1]:
        if done[i0]: continue
        L = []
        Q = [~i0, i0]
        while Q:
            i = Q.pop()
            if i < 0:
                if done[~i] == 2: continue
                done[~i] = 2
                L.append(~i)
                ###
                I[~i] = len(SCC)
                ###
                continue
            if i >= 0:
                if done[i]: continue
                done[i] = 1
            for j in iE[i]:
                if done[j]: continue
                Q.append(~j)
                Q.append(j)
        SCC.append(L)
    # return SCC, I
    
    ### �� Edge ���K�v�ȂƂ� �i��� return �������j
    # nE = [set() for _ in range(len(SCC))]
    # iE = [set() for _ in range(len(SCC))]
    ciE = [1] * len(SCC)
    for i, e in enumerate(E):
        for j in e:
            if I[i] == I[j]: continue
            # print("i, j, I[i], I[j] =", i, j, I[i], I[j])
            # nE[I[i]].add(I[j])
            # iE[I[j]].add(I[i])
            ciE[I[j]] = 0
    # nE = [list(e) for e in nE]
    # iE = [list(e) for e in iE]
    return ciE
    # return SCC, I, nE, iE, ciE

N, M = map(int, input().split())
Z = [[1 if a == "#" else 0 for a in input()] for _ in range(N)]

su = sum([int(a) for a in input().split()])

I = []
ZZ = [[-1] * M for _ in range(N)]
for j in range(M):
    for i in range(N)[::-1]:
        if Z[i][j]:
            ZZ[i][j] = len(I)
            I.append((i << 20) ^ j)
        elif i < N - 1:
            ZZ[i][j] = ZZ[i+1][j]

mmm = (1 << 20) - 1
E = [[] for _ in range(su)]
for k in range(su):
    ij = I[k]
    i = ij >> 20
    j = ij & mmm
    if i < N - 1 and ZZ[i+1][j] >= 0:
        E[k].append(ZZ[i+1][j])
    if i and Z[i-1][j]:
        E[k].append(ZZ[i-1][j])
    if j and ZZ[i][j-1] >= 0:
        E[k].append(ZZ[i][j-1])
    if j < M - 1 and ZZ[i][j+1] >= 0:
        E[k].append(ZZ[i][j+1])

ciE = scc(E)

print(sum(ciE))



