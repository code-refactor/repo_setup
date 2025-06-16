#!/usr/bin/env python3

a = int(input())
d = {}
f = {}
for i in range(a*(a-1)//2-1):
    v, c = map(int, input().split())
    if v not in f:
        f[v] = []
    f[v].append(c)
    if v in d:
        d[v] += 1
    else:
        d[v] = 1
    if c in d:
        d[c] += 1
    else:
        d[c] = 1
s = []
m = 0
for i in range(1, a + 1):
    if d[i] > m:
         m = d[i]
for i in range(1, a + 1):
    if d[i] < m:
        s.append(i)
m = 0
for i in range(1, a + 1):
    if i not in s:
        if s[0] in f and i in f and s[1] in f:
            if i in f[s[1]] and s[0] in f[i]:
                m = 1
                s.reverse()
                break
print(*s)