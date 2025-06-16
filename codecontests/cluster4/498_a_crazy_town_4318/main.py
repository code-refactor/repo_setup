#!/usr/bin/env python3

x1,y1 = [int(i) for i in input().split()]
x2,y2 = [int(i) for i in input().split()]
n = int(input())
m = 0
for i in range(n):
    x,y,c = [int(g) for g in input().split()]
    if(x1*x+y1*y+c>0):
        l = 1
    else:
        l = -1
    if(l==-1)and(x2*x+y2*y+c>0):
        m+=1
    elif(l==1)and(x2*x+y2*y+c<0):
        m+=1
print(m)
