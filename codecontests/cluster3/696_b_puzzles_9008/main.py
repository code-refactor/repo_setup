#!/usr/bin/env python3

import sys
sys.path.append('..')

n = int(input())
if n ==1:
    print(1)
    exit(0)
l = list(map(int,input().split()))
w = [[]for i in range(n)]
sz = [1]*n
for i in range(n-1):
    w[l[i]-1].append(i+1)
for i in range(n-1,-1,-1):
    for j in range(len(w[i])):
        sz[i]+=sz[w[i][j]]
ans = [0]*n
for i in range(n):
    for j in range(len(w[i])):
        ans[w[i][j]] = ans[i]+1+(sz[i]-1-sz[w[i][j]])/2
for i in range(n):
    print(ans[i]+1,end = " ")