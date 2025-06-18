#!/usr/bin/env python3

n, s = map(int, input().split())
a = [0] * n
if n == 2:
    xc, xd = map(int, input().split())
    print(s)
    exit()
for i in range(n - 1):
    xc, xd = map(int, input().split())
    a[xd - 1] += 1
    a[xc - 1] += 1
cnt = 0
for i in range(n):
    if a[i] == 1:
        cnt += 1
print(2 * round(s / cnt, 10))