#!/usr/bin/env python3

def fun(a,b):
    if a % b != 0:
        return -1
    temp = 0
    m = a/b
    
    while m % 2 == 0:
        m = m / 2
        temp += 1
    while m % 3 == 0:
        m = m/3
        temp += 1
    if m == 1:
        return temp
    else :
        return -1
a,b = map(int,input().split())
print(fun(b,a))