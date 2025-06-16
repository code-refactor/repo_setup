#!/usr/bin/env python3

import sys
p = sys.stdin.read().split()
n, t = int(p[0]), p[1][::-1]
d = {q.lower(): q for q in p[3:]}
k, s = 0, []
l = sorted(set(map(len, d)))
while n:
    k -= 1
    if len(l) + k < 0: k, n = s.pop()
    elif n >= l[k] and t[n - l[k]:n] in d:
        s.append((k, n))
        n -= l[k]
        k = 0
print(*[d[t[n - l[i]:n]] for i, n in s])