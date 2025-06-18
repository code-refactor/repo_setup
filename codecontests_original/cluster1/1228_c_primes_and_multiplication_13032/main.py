#!/usr/bin/env python3

"""

import math

MOD=1000000007

def powr(n,N):
    temp=1
    while(N>0):
        if(N%2!=0):
            temp=(temp*n)%MOD
        n=(n*n)%MOD
        N=N//2
    return (temp%MOD)

x,n=map(int,input().split())

n1=x
L=[]
while(n1%2==0): 
    L.append(2) 
    n1=n1//2

for i in range(3,int(math.sqrt(n1))+1,2): 

    while(n1%i==0): 
        L.append(i) 
        n1=n1//i 
 
if(n1>2): 
    L.append(n1)

L=list(set(L))
mul=1
for i in range(0,len(L)):
    d=L[i]
    nn=n
    tot=0
    while(nn>0):
        tot=(tot+(nn//d))%MOD
        nn=(nn//d)%MOD

    mul=(mul*powr(d,tot))%MOD

print(mul)
"""
"""

import math

MOD=1000000007

def powr(n,N):
    temp=1
    while(N>0):
        if(N%2!=0):
            temp=(temp*n)%MOD
        n=(n*n)%MOD
        N=N//2
    return (temp%MOD)

def MODI(a,b):
    ans=(powr(a,b)%MOD)
    return ans
 

x,n=map(int,input().split())

n1=x
L=[]
while(n1%2==0): 
    L.append(2) 
    n1=n1//2

for i in range(3,int(math.sqrt(n1))+1,2): 

    while(n1%i==0): 
        L.append(i) 
        n1=n1//i 
 
if(n1>2): 
    L.append(n1)

L=list(set(L))
mul=1
for i in range(0,len(L)):
    d=L[i]
    t=MODI(d,MOD-2)%MOD
    nn=n
    while(nn>0):
        rem=nn%d
        nn=(nn-rem)%MOD
        nn=(nn*t)%MOD
        mul=(mul*powr(d,nn))%MOD

    

print(mul)

"""

import math

MOD=1000000007

def powr(n,N):
    temp=1
    while(N>0):
        if(N%2!=0):
            temp=(temp*n)%MOD
        n=(n*n)%MOD
        N=N//2
    return (temp%MOD)

x,n=map(int,input().split())

n1=x
L=[]
while(n1%2==0): 
    L.append(2) 
    n1=n1//2

for i in range(3,int(math.sqrt(n1))+1,2): 

    while(n1%i==0): 
        L.append(i) 
        n1=n1//i 
 
if(n1>2): 
    L.append(n1)

L=list(set(L))
mul=1
for i in range(0,len(L)):
    d=L[i]
    nn=n
    while(nn>0):
        mul=(mul*powr(d,nn//d))%MOD
        nn=nn//d

print(mul)

