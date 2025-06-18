#!/usr/bin/env python3

import sys
from library import read_str

s = read_str()
N = len(s)
if len(s) == 1:
    print(1, s[0])
    sys.exit()
X = [s[-1], s[-2]+s[-1] if s[-2]!=s[-1] else ""]
Y = [1, 2 if s[-2]!=s[-1] else 0]
for i in range(N-3, -1, -1):
    c = s[i]
    k1 = c+X[-1]
    ng = Y[-1]+1
    if ng > 10:
        k1 = k1[:5] + "..." + k1[-2:]
    if c == s[i+1] and k1 > X[-2]:
        k1 = X[-2]
        ng = Y[-2]
    X.append(k1)
    Y.append(ng)
for i in range(N-1, -1, -1):
    print(Y[i], X[i])