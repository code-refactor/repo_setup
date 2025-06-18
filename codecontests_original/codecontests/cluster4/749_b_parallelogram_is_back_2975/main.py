#!/usr/bin/env python3

a=list(map(int, input().split()))
x1=a[0]
y1=a[1]
a=list(map(int, input().split()))
x2=a[0]
y2=a[1]
a=list(map(int, input().split()))
x3=a[0]
y3=a[1]
print(3)
print(x1+x2-x3, y1+y2-y3)
print(x1+x3-x2, y1+y3-y2)
print(x3+x2-x1, y2+y3-y1)
       
