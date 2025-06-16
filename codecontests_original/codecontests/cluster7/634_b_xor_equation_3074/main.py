#!/usr/bin/env python3

s,x=map(int,input().split())
if x>s or (s-x)%2!=0:
    print(0)
else:
    mask=1
    res=1
    bit=0
    ND=(s-x)//2
    flag=False
    while bit<50:
        if (mask&x)>0:
            res*=2
        if mask&x>0 and ND&mask>0:
            flag=True
            break
        mask*=2
        bit+=1
    if(s==x):
        res-=2
    if flag:
        res=0
    print(res)
    