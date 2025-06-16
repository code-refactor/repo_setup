#!/usr/bin/env python3

from math import pow
def take_input(s):          #for integer inputs
    if s == 1:  return int(input())
    return map(int, input().split())

def factor(n,k):
    i = 0
    while(n%k==0):
        i += 1
        n //= k
    return i
        
a, b = take_input(2)
count = 0
if a == b:
    print(0)
    exit()

a_fac_2 = factor(a,2); a_fac_3 = factor(a,3); a_fac_5 = factor(a,5)
b_fac_2 = factor(b,2); b_fac_3 = factor(b,3); b_fac_5 = factor(b,5)
x = a
if a_fac_2>0:   x //= pow(2,a_fac_2)
if a_fac_3>0:   x //= pow(3,a_fac_3)
if a_fac_5>0:   x //= pow(5,a_fac_5)
y = b
if b_fac_2>0:   y //= pow(2,b_fac_2)
if b_fac_3>0:   y //= pow(3,b_fac_3)
if b_fac_5>0:   y //= pow(5,b_fac_5)


if x != y:
    print(-1)
else:
    print(abs(a_fac_2 - b_fac_2) + abs(a_fac_3 - b_fac_3) + abs(a_fac_5 - b_fac_5))
