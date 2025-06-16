#!/usr/bin/env python3

import os
import sys
from io import BytesIO, IOBase
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
input = lambda: sys.stdin.readline()
 
# ------------------------------

def RL(): return map(int, sys.stdin.readline().split())
def RLL(): return list(map(int, sys.stdin.readline().split()))
def N(): return int(input())
def print_list(l):
    print(' '.join(map(str,l)))
    
# sys.setrecursionlimit(100000)
# import random
# from functools import reduce
# from functools import lru_cache
# from heapq import *
# from collections import deque as dq
# from math import ceil,floor,sqrt,pow,gcd,log
# import bisect as bs
# from collections import Counter
# from collections import defaultdict as dc 

for _ in range(N()):
    n = N()
    dic = [[] for _ in range(n + 1)]
    gress = [0] * (n + 1)
    gress[1] += 1
    father = [0] * (n + 1)
    for _ in range(n - 1):
        u, v = RL()
        dic[u].append(v)
        dic[v].append(u)
    now = [1]
    s = [[] for _ in range(n + 1)]
    leaf = []
    while now:
        node = now.pop()
        for child in dic[node]:
            if child != father[node]:
                gress[node] += 1
                father[child] = node
                now.append(child)
        if gress[node] == 0:
            leaf.append(node)
    while leaf:
        node = leaf.pop()
        f = father[node]
        if not s[node]:
            s[f].append((1, 0))
        elif len(s[node]) == 1:
            d, k = s[node][0]
            s[f].append((d + 1, k))
        else:
            d = min(p[0] for p in s[node]) + 1
            k = max(max(p[1] for p in s[node]), max(p[0] for p in s[node]) + 1)
            s[f].append((d, k))
        gress[f] -= 1
        if gress[f] == 0:
            leaf.append(f)
    node = 1
    if len(s[node]) == 1:
        print(max(s[node][0]))
    else:
        k = max(p[1] for p in s[node])
        tmp = [p[0] for p in s[node]]
        m = max(tmp)
        tmp.remove(m)
        print(max(max(tmp)+1, m, k))

    # print(s)