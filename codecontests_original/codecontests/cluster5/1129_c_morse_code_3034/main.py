#!/usr/bin/env python3

import os, sys
nums = list(map(int, os.read(0, os.fstat(0).st_size).split()))

MOD = 10 ** 9 + 7
BAD = ([0, 0, 1, 1], [0, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1])

def zfunc(s):
    z = [0] * len(s)
    l = r = 0
    for i in range(1, len(s)):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < len(s) and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z

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
                f[j] = (f[j] + f[k + 1])%MOD
    z = zfunc(s[::-1])
    new = i - max(z)
    for x in f[:new]:
        sm = (sm + x)%MOD
    ans.append(sm)
print(*ans, sep='\n')