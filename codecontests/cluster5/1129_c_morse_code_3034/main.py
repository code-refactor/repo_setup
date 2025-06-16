#!/usr/bin/env python3

import os, sys
from library import z_function, MOD1

nums = list(map(int, os.read(0, os.fstat(0).st_size).split()))

BAD = ([0, 0, 1, 1], [0, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1])

n = nums[0]
s = []
sm = 0
ans = []
for i in range(1, n + 1):
    s.append(nums[i])
    cur = 0
    f = [0] * (i + 1)
    f[i] = 1
    for j in range(i - 1, -1, -1):
        for k in range(j, min(j + 4, i)):
            if s[j : k + 1] not in BAD:
                f[j] = (f[j] + f[k + 1])%MOD1
    z = z_function(s[::-1])
    new = i - max(z)
    for x in f[:new]:
        sm = (sm + x)%MOD1
    ans.append(sm)
print(*ans, sep='\n')