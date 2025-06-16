#!/usr/bin/env python3

import sys
from library import gcd, normalize_slope
from collections import defaultdict
input=sys.stdin.readline
n=int(input())
p=[list(map(int,input().split())) for i in range(n)]
ans=0
for xi,yi in p:
    angle=defaultdict(int)
    for x,y in p:
        if xi==x and yi==y:
            continue
        x-=xi;y-=yi
        angle[normalize_slope(x,y)]+=1
    cnt=0
    for i in angle.keys():
        cnt+=angle[i]*(n-1-angle[i])
    ans+=cnt//2
print(ans//3)