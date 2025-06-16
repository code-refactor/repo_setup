#!/usr/bin/env python3

from library import read_ints, distance_squared

a,b=read_ints()
a,b=min(a,b),max(a,b)
l1=[]
l2=[]
for i in range(1,a):
    t=(a*a-i*i)**0.5
    if(int(t)==t):
        l1.append([int(t),i])
for i in range(1,b):
    t=(b*b-i*i)**0.5
    if(int(t)==t):
        l2.append([int(t),-i])

found = False
for i in range(len(l1)):
    if found:
        break
    for j in range(len(l2)):
        x1,y1 = l1[i]
        x2,y2 = l2[j]
        if x1!=x2 and distance_squared((x1,y1),(x2,y2)) == a*a+b*b:
            found = True
            print("YES")
            print("0   0")
            print(f"{x1}   {y1}")
            print(f"{x2}   {y2}")
            break
if not found:
    print("NO")