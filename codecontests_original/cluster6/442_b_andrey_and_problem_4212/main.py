#!/usr/bin/env python3

n=int(input())
from itertools import combinations

a = sorted(list(map(float, input().split())), reverse=True)
#a=[0.01]*100
if max(a) == 1:
    print(1)
    quit()
n=len(a)
pre = [1]*100
pre[0] = 1 - a[0]
for i in range(1, n):
    pre[i] = pre[i-1] * (1-a[i])

ans = 0
for i in range(1,n+1):
    anss=0
    for j in range(i):
        anss = anss + pre[i-1] / (1-a[j]) * a[j]
    ans = max(ans, anss)
print(ans)