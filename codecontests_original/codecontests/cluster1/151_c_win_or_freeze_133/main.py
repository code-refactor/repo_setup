#!/usr/bin/env python3

import sys
line = sys.stdin.readline()
N = int(line)
tmp = N
factor = []
i = 2
while i**2 <= tmp:
    if tmp % i == 0:
        tmp //= i
        factor.append(i)
    else: i += 1
if tmp != 1: factor.append(i)
if len(factor) == 2: print(2)
else:
    print(1)
    if len(factor) <= 1: print(0)
    else: print(factor[0] * factor[1])