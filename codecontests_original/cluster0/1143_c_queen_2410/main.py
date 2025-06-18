#!/usr/bin/env python3

"""
https://codeforces.com/problemset/problem/1143/C
"""

n = int(input())

respect = [0 for _ in range(n)]
child_respect = [0 for _ in range(n)]

root = -1

for i in range(n):
    p, c = map(int,input().split())
    if p == -1:
        root = i
        continue
    respect[i] = c
    if p != -1 and not c: child_respect[p-1]=1

res = []
for i in range(n):
    if i == root:
        continue
    if respect[i] and not child_respect[i]:
        res.append(i+1)

if res:
    print(*res)
else:
    print(-1)