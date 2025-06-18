#!/usr/bin/env python3

import sys
import string
input = sys.stdin.readline
import math
#import numpy
#letters = list(string.ascii_lowercase)
from decimal import Decimal

n = list(map(int, input().split()))
n,k = n[0], n[1]
m = 998244353

fact = []
fac = 1

for i in range(1, n+2):
    fac *= i
    fac = fac % m
    fact.append(fac)

ans = 0
fact = [1] + fact

for i in range(1, n//k + 1):
    out = n//k
    a = n//i - 1
    b = k - 1
    #print(a,b)
    #print(pow(2,6, 502))
    l = fact[b] * fact[a-b]
    ans += (fact[a] * pow(l, m-2, m)) % m
    #print(ans)
    #print(i, ans)
    
print(int(ans) % m)