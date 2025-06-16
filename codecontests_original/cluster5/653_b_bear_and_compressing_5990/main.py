#!/usr/bin/env python3

# You lost the game.
n, q = map(int, input().split())
L = [list(str(input()).split(" ")) for _ in range(q)]
A = [[] for _ in range(6)]
B = "abcdef"
for i in range(q):
    e = B.index(L[i][1])
    A[e]  = A[e] + [L[i][0]]
R = [1,0,0,0,0,0]
for i in range(1,n):
    K = [0,0,0,0,0,0]
    for j in range(6):
        for k in A[j]:
            e = B.index(k[0])
            K[e] += R[j]
    R = K[:]
print(sum(R))