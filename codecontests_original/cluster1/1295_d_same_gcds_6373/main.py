#!/usr/bin/env python3

import sys, math

for ii in range(int(input())):
    a,m = map(int,input().split())
    g = math.gcd(a,m)
    m=int(m/g)
    ans = m
    for i in range(2,int(math.sqrt(m))+1):
        if m%i==0:
            ans-=(ans/i)
        while m%i==0:
            m=int(m/i)
    if m>1:
        ans-=ans/m
    print(int(ans))
#3SUPE