#!/usr/bin/env python3

from fractions import *
n,L=int(input()),0
while (n%2==0):n,L=n//2,L+1
if (n==1):print('%d/1'%L)
else:
    s,t=1,1
    for i in range(n):
        t=t*2%n
        s*=2
        if (t==1):
            m=i+1
            break
    r,t,i,ans=s,s*n,L,0
    while (r>1):
        i,t=i+1,t//2
        if (r-t>0):
            r,ans=r-t,ans+i*t
    print((Fraction(ans,s)+Fraction(m,s))/(1-Fraction(1,s)))
