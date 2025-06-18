#!/usr/bin/env python3

from library import read_ints, read_strs, init_dp_1d

n, q = read_ints()
L = [read_strs() for _ in range(q)]
A = [[] for _ in range(6)]
B = "abcdef"

for i in range(q):
    e = B.index(L[i][1])
    A[e] = A[e] + [L[i][0]]

R = init_dp_1d(6, 0)
R[0] = 1  # Initialize only 'a' as 1

for i in range(1, n):
    K = init_dp_1d(6, 0)
    for j in range(6):
        for k in A[j]:
            e = B.index(k[0])
            K[e] += R[j]
    R = K[:]

print(sum(R))