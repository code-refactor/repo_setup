#!/usr/bin/env python3

n = int(input())
p = list(map(int,input().split()))
MOD = 10**9+7

mode = 0
if n%4 == 3:
    n-= 1
    new = []
    for i in range(n):
        if mode == 0: new.append(p[i]+p[i+1])
        else: new.append(p[i]-p[i+1])
        mode = 1-mode
    p = new

def calc0(p):
    res = 0
    ncr = 1
    n = len(p)//2-1
    for i in range(n+1):
        res = (res+ncr*(p[i*2]-p[i*2+1])) % MOD
        ncr = (ncr*(n-i)*pow(i+1,MOD-2,MOD)) % MOD
    return res

def calc1(p):
    res = 0
    ncr = 1
    n = len(p)//2
    for i in range(n+1):
        res = (res+ncr*(p[i*2])) % MOD
        ncr = (ncr*(n-i)*pow(i+1,MOD-2,MOD)) % MOD
    return res

def calc2(p):
    res = 0
    ncr = 1
    n = len(p)//2-1
    for i in range(n+1):
        res = (res+ncr*(p[i*2]+p[i*2+1])) % MOD
        ncr = (ncr*(n-i)*pow(i+1,MOD-2,MOD)) % MOD
    return res

print([calc0,calc1,calc2,-1][n%4](p))