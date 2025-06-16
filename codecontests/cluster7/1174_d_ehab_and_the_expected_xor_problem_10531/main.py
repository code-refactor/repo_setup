#!/usr/bin/env python3

import sys
sys.path.append('..')
from library import read_ints

n, x = read_ints()
ans = []
vis = [0] * ((2 ** 18) + 1)
lmt = 2 ** n
xor = 0
vis[0], vis[x] = 1, 1
for i in range(1, lmt):
    if vis[i]:
        continue
    ans.append(xor ^ i)
    xor = i
    vis[i] = 1
    vis[i ^ x] = 1
print(len(ans))
print(*ans)
    
