#!/usr/bin/env python3

from bisect import insort,bisect_right,bisect_left
from sys import stdout, stdin, setrecursionlimit
from math import sqrt,ceil,floor,factorial,gcd,log2,log10
from io import BytesIO, IOBase
from collections import *
from itertools import *
from random import * 
from string import *
from queue import *
from heapq import heappush, heappop, heapify 
from re import *
from os import *

####################################---fast-input-output----#########################################


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = read(self._fd, max(fstat(self._fd).st_size, 8192))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = read(self._fd, max(fstat(self._fd).st_size, 8192))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


stdin, stdout = IOWrapper(stdin), IOWrapper(stdout)
graph, mod, szzz =  {}, 10**9 + 7, lambda: sorted(zzz())
def getStr(): return input()
def getInt(): return int(input())
def listStr(): return list(input())
def getStrs(): return input().split()
def isInt(s): return '0' <= s[0] <= '9'
def input(): return stdin.readline().strip()
def zzz(): return [int(i) for i in input().split()]
def output(answer, end='\n'): stdout.write(str(answer) + end)
def lcd(xnum1, xnum2): return (xnum1 * xnum2 // gcd(xnum1, xnum2))


def getPrimes(N = 10**5):
    SN = int(sqrt(N))
    sieve = [i for i in range(N+1)]
    sieve[1] = 0
    for i in sieve:
        if i > SN:
            break
        if i == 0:
            continue
        for j in range(2*i, N+1, i):
            sieve[j] = 0
    prime = [i for i in range(N+1) if sieve[i] != 0] 
    return prime
def primeFactor(n,prime=getPrimes()):
    lst = []
    mx=int(sqrt(n))+1
    for i in prime:
        if i>mx:break
        while n%i==0:
            lst.append(i)
            n//=i
    if n>1:
        lst.append(n)
    return lst    

dx = [-1, 1, 0, 0, 1, -1, 1, -1]
dy = [0, 0, 1, -1, 1, -1, -1, 1]
daysInMounth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


#################################################---Some Rule For Me To Follow---#################################
"""
    --instants of Reading problem continuously try to understand them.

    --If you Know some-one , Then you probably don't know him !

    --Try & again try, maybe you're just one statement away!


"""
##################################################---START-CODING---###############################################


s = n = getInt()+1
lst,new=[],list(range(n))[::-1]
k = 2**20
while s:
    while k>=2*s:k//=2
    lst=new[n-s:n+s-k]+lst
    s=k-s

print(n*(n-1))
print(' '.join(map(str, lst)))





