#!/usr/bin/env python3

from library import read_ints, read_int

x1, y1 = read_ints()
x2, y2 = read_ints()
n = read_int()
m = 0
for i in range(n):
    x, y, c = read_ints()
    if(x1*x+y1*y+c>0):
        l = 1
    else:
        l = -1
    if(l==-1)and(x2*x+y2*y+c>0):
        m+=1
    elif(l==1)and(x2*x+y2*y+c<0):
        m+=1
print(m)
