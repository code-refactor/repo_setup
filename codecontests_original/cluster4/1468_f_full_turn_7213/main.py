#!/usr/bin/env python3

import os
import sys
from io import BytesIO, IOBase
# region fastio
BUFSIZE = 8192
class FastIO(IOBase):
    def __init__(self, file):
        self.newlines = 0
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
 
# --------------------------------------------------------------------

def RL(): return map(int, sys.stdin.readline().split())
def RLL(): return list(map(int, sys.stdin.readline().split()))
def N(): return int(input())
def S(): return input().strip()
def print_list(l): print(' '.join(map(str, l)))
    
# sys.setrecursionlimit(100000)
# import random
# from functools import reduce
# from functools import lru_cache
# from heapq import *
# from collections import deque as dq
from math import gcd
# import bisect as bs
from collections import Counter
# from collections import defaultdict as dc 

for _ in range(N()):
    dic = Counter()
    for _ in range(N()):
        x, y, u, v = RL()
        dx, dy = u - x, v - y 
        if dx == 0:
            dic[(0, 1 if dy > 0 else -1)] += 1
        elif dy == 0:
            dic[(1 if dx > 0 else -1, 0)] += 1
        else:
            t = gcd(dx, dy)
            dic[(dx // t, dy // t)] += 1
    print(sum(dic[(x, y)] * dic[(-x, -y)] for x, y in dic) >> 1)
