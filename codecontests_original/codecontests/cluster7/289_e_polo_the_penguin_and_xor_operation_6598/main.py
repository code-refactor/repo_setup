#!/usr/bin/env python3

import sys
from math import gcd,sqrt,ceil
from collections import defaultdict,Counter,deque
from bisect import bisect_left,bisect_right
import math
from itertools import permutations

# input=sys.stdin.readline
# def print(x):
#     sys.stdout.write(str(x)+"\n")

# sys.stdin = open('input.txt', 'r')
# sys.stdout = open('output.txt', 'w')
import os
import sys
from io import BytesIO, IOBase

BUFSIZE = 8192


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")

# import sys
# import io, os
# input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
def get_sum(bit,i):
    s = 0

    i+=1
    while i>0:
        s+=bit[i]
        i-=i&(-i)

    return s

def update(bit,n,i,v):
    i+=1

    while i<=n:
        bit[i]+=v
        i+=i&(-i)


def modInverse(b,m):
    g = math.gcd(b, m)
    if (g != 1):
        return -1
    else:
        return pow(b, m - 2, m)

def primeFactors(n):

    sa = set()
    sa.add(n)
    while n % 2 == 0:
        sa.add(2)
        n = n // 2


    for i in range(3,int(math.sqrt(n))+1,2):


        while n % i== 0:
            sa.add(i)
            n = n // i

    # sa.add(n)
    return sa


def seive(n):

    pri = [True]*(n+1)
    p = 2
    while p*p<=n:

        if pri[p] == True:

            for i in range(p*p,n+1,p):
                pri[i] = False

        p+=1

    return pri

def debug(n):
    l = [i for i in range(n+1)]
    z = permutations(l)
    maxi = 0
    for i in z:
        fin = 0
        for j in range(n+1):
            fin+=j^i[j]

        maxi = max(maxi,fin)

    return maxi


n = int(input())
hash = defaultdict(int)
ans = [0]*(n+1)
seti = set()
for i in range(n,0,-1):
    if i not in seti:
       z1 = i^int('1'*len((bin(i)[2:])),2)

       seti.add(z1)
       ans[z1] = i
       ans[i] = z1
       # print(ans)

fin = 0
for i in range(n+1):
    fin+=i^ans[i]
print(fin)
print(*ans)



