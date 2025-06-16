#!/usr/bin/env python3

import os
import sys
from io import BytesIO, IOBase


def main():
    pass


# region fastio

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
def count1(s):
    c=0
    for i in s:
        if(i=='1'):
            c+=1
    return(c)
def binary(n):
    return(bin(n).replace("0b",""))
def decimal(s):
    return(int(s,2))
def pow2(n):
    p=0
    while(n>1):
        n//=2
        p+=1
    return(p)
def isPrime(n):
    if(n==1):
        return(False)
    else:
        root=int(n**0.5)
        root+=1
        for i in range(2,root):
            if(n%i==0):
                return(False)
        return(True)
a,b=map(int,input().split())
a,b=min(a,b),max(a,b)
f=False
ans=[[0,0]]
f=False
l1=[]
l2=[]
for i in range(1,a):
    t=(a*a-i*i)**0.5
    if(int(t)==t):
        l1.append([int(t),i])
for i in range(1,b):
    t=(b*b-i*i)**0.5
    if(int(t)==t):
        l2.append([int(t),-i])
f=True
for i in range(0,len(l1)):
    if(f):
        for j in range(0,len(l2)):
            x1=l1[i][0]
            x2=l2[j][0]
            y1=l1[i][1]
            y2=l2[j][1]
            if(x1!=x2 and ((y2-y1)**2+(x2-x1)**2)==(a**2+b**2)):
                f=False
                print("YES")
                print(0,0)
                print(x1,y1)
                print(x2,y2)
                break
if(f):
    print("NO")