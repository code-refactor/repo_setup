#!/usr/bin/env python3

"""n=int(input())
x=list(map(int, input().split()))
c=0
pro=1
for i in range(n):
    if x[i]==1:
        c+=1
        if c==1:
            old=i
        elif c>1:
            new=i
            pro*=(new-old)
            old=new
print(pro)
"""
from library import read_ints

a = read_ints()
b = read_ints()
c = read_ints()
x,y,z=1,1,0
if a[0]==b[0] or a[0]==c[0] or b[0]==c[0]:
    x=2
    if a[0]==b[0] and a[0]==c[0] and b[0]==c[0]:
        x=3
    else:
        if a[0]==b[0]:
            if c[1] in range(min(a[1],b[1]),max(a[1],b[1])):
                z+=1
        elif a[0]==c[0]:
            if b[1] in range(min(a[1],c[1]),max(a[1],c[1])):
                z+=1
        elif b[0]==c[0]:
            if a[1] in range(min(b[1],c[1]),max(b[1],c[1])):
                z+=1
if a[1]==b[1] or a[1]==c[1] or b[1]==c[1]:
    y=2
    if a[1]==b[1] and a[1]==c[1] and b[1]==c[1]:
        y=3
    else:
        if a[1]==b[1]:
            if c[0] in range(min(a[0],b[0]),max(a[0],b[0])):
                z+=1
        elif a[1]==c[1]:
            if b[0] in range(min(a[0],c[0]),max(a[0],c[0])):
                z+=1
        elif b[1]==c[1]:
            if a[0] in range(min(b[0],c[0]),max(b[0],c[0])):
                z+=1
if x*y==1:
    print(3)
elif x*y==3:
    print(1)
elif x*y==4:
    print(2)
else:
    if z==1:
        print(3)
    else:
        print(2)