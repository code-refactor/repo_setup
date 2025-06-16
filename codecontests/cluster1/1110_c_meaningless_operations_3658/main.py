#!/usr/bin/env python3
import math

q = int(input())
for _ in range(q):
    n = int(input())
    k = int(math.log2(n + 1))
    if (1 << k) < n + 1:
        print((1 << (k + 1)) - 1)
        continue
    else:
        found = False
        for j in range(2, int(math.sqrt(n)) + 1):
            if n % j == 0:
                print(n // j)
                found = True
                break
        if not found:
            print(1)