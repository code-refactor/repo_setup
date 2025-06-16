#!/usr/bin/env python3

R = lambda: map(int, input().split())
n = int(input())
fcs = [0] + list(R())
ps = [0, 0] + list(R())
cs = [1] * (n + 1)
for i in range(2, n + 1):
    cs[ps[i]] = 0
nc = sum(cs) - 1
for i in range(n, 1, -1):
    if fcs[ps[i]] == 0:
        cs[ps[i]] += cs[i]
    else:
        if not cs[ps[i]]:
            cs[ps[i]] = cs[i]
        else:
            cs[ps[i]] = min(cs[ps[i]], cs[i])
print(nc - cs[1] + 1)