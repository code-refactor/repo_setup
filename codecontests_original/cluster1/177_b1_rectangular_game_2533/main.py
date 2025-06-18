#!/usr/bin/env python3

n=int(input())
r=n+1
i=2
s=n**0.5
while i<=s:
    if n%i==0:
        r+=n//i
        n//=i
        s=n**0.5
        i=1
    i+=1
print(r)