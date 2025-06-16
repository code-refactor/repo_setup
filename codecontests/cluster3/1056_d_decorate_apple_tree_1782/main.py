#!/usr/bin/env python3


n = int(input())
if n == 1:
    print(1)
else:
    p = [0, 0] + list(map(int, input().split()))
    
    d = [0] * (n + 1)
    for i in range(n, 1, -1):
        if d[i] == 0:
            d[i] = 1
        d[p[i]] += d[i]
    
    d = d[1:]
    d.sort()
    print(*d)