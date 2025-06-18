#!/usr/bin/env python3

from sys import stdin, stdout
from math import sqrt
#stdin = open('Q3.txt', 'r') 
def II(): return int(stdin.readline())
def MI(): return map(int, stdin.readline().split())
bigp=10**18+7

primes=[]
def SieveOfEratosthenes(n,primes): 
    prime = [True for i in range(n+1)] 
    p = 2
    while (p * p <= n): 
        if (prime[p] == True): 
            for i in range(p * p, n+1, p): 
                prime[i] = False
        p += 1
    for p in range(2, n): 
        if prime[p]: 
            primes.append(p)

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

SieveOfEratosthenes(32000,primes)
t=II()
for _ in range(t):
    solve()