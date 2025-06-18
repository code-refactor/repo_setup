#!/usr/bin/env python3

from sys import stdin
import math
n=int(stdin.readline())
if n<3:
    k=n
else:
    d=0
    g=n
    for i in range(2,int(math.sqrt(n))+1):
        if n%i==0:
            d+=1
            g=math.gcd(g,i)
            if i*i!=n:
                d+=1
                g=math.gcd(g,n//i)
    if d==0:
        k=n
    else:
        k=g
print(k)
    



    
    