#!/usr/bin/env python3

from sys import stdin, stdout
from math import sqrt
from library import sieve
#stdin = open('Q3.txt', 'r') 
def II(): return int(stdin.readline())
def MI(): return map(int, stdin.readline().split())
bigp=10**18+7

def solve():
    p,q=MI()
    if p%q != 0:
        ans=p
    else:
        x,y=q,p
        mind=bigp
        sqrtq=int(sqrt(q))
        sp=[i for i in primes if i<=sqrtq]+[bigp]
        for i in sp:
            j=i
            if x==1:
                break
            qe=0
            while x%j==0:
                qe+=1
                x=x//j
            if i==bigp:
                qe,j=1,x
            if qe>0:
                pe=qe
                y=y//pow(j,qe)
                while y%j==0:
                    pe+=1
                    y=y//j
                mind=min(mind,pow(j,pe-qe+1))
        ans=p//mind
    stdout.write(str(ans)+"\n")

primes = sieve(32000)
t=II()
for _ in range(t):
    solve()