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
input = lambda: sys.stdin.readline().rstrip("\r\n")

# ------------------------------

from math import factorial
from collections import Counter, defaultdict
from heapq import heapify, heappop, heappush

def RL(): return map(int, sys.stdin.readline().rstrip().split())
def RLL(): return list(map(int, sys.stdin.readline().rstrip().split()))
def N(): return int(input())
def comb(n, m): return factorial(n) / (factorial(m) * factorial(n - m)) if n >= m else 0
def perm(n, m): return factorial(n) // (factorial(n - m)) if n >= m else 0
def mdis(x1, y1, x2, y2): return abs(x1 - x2) + abs(y1 - y2)
def ctd(chr): return ord(chr)-ord("a")
mod = 998244353
INF = float('inf')
from heapq import heappush, heappop

# ------------------------------
# f = open('./input.txt')
# sys.stdin = f

def main():
    n, m = RL()
    x, y = RL()
    gp = defaultdict(dict)

    for _ in range(m):
        u, v, w = RL()
        gp[u][v] = min(gp[u].get(v, INF), w)
        gp[v][u] = min(gp[v].get(u, INF), w)

    cars = [[0, 0]]
    for _ in range(n):
        t, c = RL()
        cars.append([t, c])

    disarr = [[INF]*(n+1) for _ in range(n+1)]
    for i in range(1, n+1):
        disarr[i][i] = 0

    newg = [[INF]*(n+1) for _ in range(n+1)]
    dnex = defaultdict(list)

    def dij(s):
        q = [(0, s)]

        while q:
            d, nd = heappop(q)

            for nex in gp[nd]:
                dis = gp[nd][nex]+disarr[s][nd]
                if dis<disarr[s][nex]:
                    disarr[s][nex] = dis
                    heappush(q, (dis, nex))

        for i in range(1, n+1):
            cd, cc = cars[s]
            d = disarr[s][i]
            if d<=cd:
                newg[s][i] = min(newg[s][i], cc)
                dnex[s].append(i)

    def dij1(s):
        q = [(0, s)]
        cst = [INF] * (n + 1)
        cst[s] = 0

        while q:
            d, nd = heappop(q)

            for nex in dnex[nd]:
                cs = cst[nd]+newg[nd][nex]
                if cs<cst[nex]:
                    cst[nex] = cs
                    heappush(q, (cs, nex))

        if cst[y]==INF:
            print(-1)
        else:
            print(cst[y])


    for i in range(1, n+1):
        dij(i)
    dij1(x)

    # for i in newg:print(i)




if __name__ == "__main__":
    main()
