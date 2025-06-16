#!/usr/bin/env python3

import os
import sys
if os.path.exists(r'C:\Users\User\codeforces'):
    f = iter(open('A.txt').readlines())
    def input():
        return next(f).strip()
    # input = lambda: sys.stdin.readline().strip()
else:
    input = lambda: sys.stdin.readline().strip()

fprint = lambda *args: print(*args, flush=True)


from math import sqrt
n, l = map(int, input().split())
x, b = [0], [0]
for _ in range(n):
    u, v = map(int, input().split())
    x.append(u)
    b.append(v)

def check(V):
    values = [2*10**9] * (n+1)
    values[0] = 0
    for i in range(1, n+1):
        for p in range(i):
            values[i] = min(values[i], values[p] + sqrt(abs(x[i]-x[p]-l)) - V * b[i])
    return values[-1] <= 0

def get(V):
    values = [2*10**9] * (n+1)
    values[0] = 0
    prev = [-1] * (n+1)
    for i in range(1, n+1):
        for p in range(i):
            q = values[p] + sqrt(abs(x[i]-x[p]-l)) - V * b[i]
            if q < values[i]:
                prev[i] = p
                values[i] = q
    res = [n]
    while res[-1] != 0:
        res.append(prev[res[-1]])
    res.pop()
    return res

eps = 1e-9
R, L = 10**3+1, 0
while R - L > eps:
    # print(R, L)
    m = (R+L)/2
    if check(m):
        R = m
    else:
        L = m

print(' '.join(map(str, reversed(get(R)))))