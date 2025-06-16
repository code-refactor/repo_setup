#!/usr/bin/env python3

import sys
import math
from heapq import *;
input = sys.stdin.readline
from functools import cmp_to_key;

def pi():
    return(int(input()))
def pl():
    return(int(input(), 16))
def ti():
    return(list(map(int,input().split())))
def ts():
    s = input()
    return(list(s[:len(s) - 1]))
def invr():
    return(map(int,input().split()))
mod = 1000000007;
f = [];
def fact(n,m):
    global f;
    f = [1 for i in range(n+1)];
    f[0] = 1;
    for i in range(1,n+1):
        f[i] = (f[i-1]*i)%m;

def fast_mod_exp(a,b,m):
    res = 1;
    while b > 0:
        if b & 1:
            res = (res*a)%m;
        a = (a*a)%m;
        b = b >> 1;
    return res;

def inverseMod(n,m):
    return fast_mod_exp(n,m-2,m);

def ncr(n,r,m):
    if n < 0 or r < 0 or r > n: return 0;
    if r == 0: return 1;
    return ((f[n]*inverseMod(f[n-r],m))%m*inverseMod(f[r],m))%m;

def main():
    E();

mp = [{''} for i in range(300005)];
def canConnect(a,b):
    return b not in mp[a];

remaining = {''};
def dfs(a):
    temp = [];
    for b in remaining:
        if canConnect(a,b): temp.append(b);
    for b in temp:
        remaining.remove(b);
    for b in temp:
        dfs(b);

def E():
    [n,m,k] = ti();
    mxDegreePossible = n-1;
    for i in range(m):
        [a,b] = ti();
        mp[a].add(b);
        mp[b].add(a);
        if a == 1 or b == 1:
            mxDegreePossible -= 1;
    
    if mxDegreePossible < k:
        print("impossible");
        return;

    for i in range(2,n+1):
        remaining.add(i);
    
    components = 0;
    for i in range(2,n+1):
        if i in remaining and canConnect(1,i):
            remaining.remove(i);
            dfs(i);
            components += 1;
    remaining.remove('');
    if components > k or len(remaining) > 0:
        print('impossible');
        return;
    print('possible');

    
    
    
main();