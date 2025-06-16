#!/usr/bin/env python3

from library import FastIO

X = [FastIO.read_ints() for _ in range(10)]
Y = [(i//10, 9-i%10 if (i//10)&1 else i%10) for i in range(100)]
Z = [[i * 10 + 9 - j if i & 1 else i * 10 + j for j in range(10)] for i in range(10)]
E = [0] * 100
F = [0] * 100
for i in range(1, 6):
    F[i] = E[i] = (sum(E[:i]) + 6) / i
for i in range(6, 100):
    F[i] = E[i] = sum(F[i-6:i])/6 + 1
    x, y = Y[i]
    if X[x][y]: F[i] = min(E[i], E[Z[x-X[x][y]][y]])

print(F[99])