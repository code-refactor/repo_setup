#!/usr/bin/env python3

from library import cross_product, read_int, read_ints

vector = lambda A, B: (B[0] - A[0], B[1] - A[1])
n = read_int()
p = [tuple(read_ints()) for i in range(n)]
cnt = 0
for i in range(2, n):
    v1 = vector(p[i], p[i - 1])
    v2 = vector(p[i - 1], p[i - 2])
    if cross_product(v1, v2) < 0:
        cnt += 1
print(cnt)
