#!/usr/bin/env python3

n=int(input())
a=list(map(int,(input().split(' '))))
a=sorted(a)
a.append(0)
ans=1
t=0
while a[3+t]==a[2]:t=t+1
if a[3]==a[0]:ans=(t+3)*(t+2)*(t+1)/6
elif a[3]==a[1]:ans=(t+2)*(t+1)/2
elif a[3]==a[2]:ans=t+1
print(int(ans))
