#!/usr/bin/env python3

from library import z_function, MOD, read_int

BAD = ([0, 0, 1, 1], [0, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1])

n = read_int()
s = []
sm = 0
ans = []

for i in range(n):
    s.append(int(input()))
    cur = 0
    f = [0] * (i + 1)
    f[i] = 1
    for j in range(i - 1, -1, -1):
        for k in range(j, min(j + 4, i)):
            if s[j : k + 1] not in BAD:
                f[j] = (f[j] + f[k + 1]) % MOD
    z = z_function(s[::-1])
    new = i - max(z)
    for x in f[:new]:
        sm = (sm + x) % MOD
    ans.append(sm)

print(*ans, sep='\n')