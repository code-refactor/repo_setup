#!/usr/bin/env python3

n = int(input())
p = n
arr = []
while p%2==0:
    arr.append(2)
    p = p//2
x = int(p**0.5)+1
for i in range(3,x,2):
    while p%i==0:
        arr.append(i)
        p = p//i
if p>2:
    arr.append(p)
if n==1 or len(arr)==1:
    print(1)
    print(0)
elif len(arr)==2:
    print(2)
else:
    x = arr[0]*arr[1]
    print(1)
    print(x)