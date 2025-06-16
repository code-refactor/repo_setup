#!/usr/bin/env python3

import sys
import math
import heapq
import bisect
from collections import Counter
from collections import defaultdict
from io import BytesIO, IOBase
import string


class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        import os
        self.os = os
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None
        self.BUFSIZE = 8192

    def read(self):
        while True:
            b = self.os.read(self._fd, max(self.os.fstat(self._fd).st_size, self.BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = self.os.read(self._fd, max(self.os.fstat(self._fd).st_size, self.BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            self.os.write(self._fd, self.buffer.getvalue())
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


def get_int():
    return int(input())


def get_ints():
    return list(map(int, input().split(' ')))


def get_int_grid(n):
    return [get_ints() for _ in range(n)]


def get_str():
    return input().split(' ')


def yes_no(b):
    if b:
        return "YES"
    else:
        return "NO"


def binary_search(good, left, right, delta=1, right_true=False):
    """
    Performs binary search
    ----------
    Parameters
    ----------
    :param good: Function used to perform the binary search
    :param left: Starting value of left limit
    :param right: Starting value of the right limit
    :param delta: Margin of error, defaults value of 1 for integer binary search
    :param right_true: Boolean, for whether the right limit is the true invariant
    :return: Returns the most extremal value interval [left, right] which is good function evaluates to True,
            alternatively returns False if no such value found
    """

    limits = [left, right]
    while limits[1] - limits[0] > delta:
        if delta == 1:
            mid = sum(limits) // 2
        else:
            mid = sum(limits) / 2
        if good(mid):
            limits[int(right_true)] = mid
        else:
            limits[int(~right_true)] = mid
    if good(limits[int(right_true)]):
        return limits[int(right_true)]
    else:
        return False


def prefix_sums(a, drop_zero=False):
    p = [0]
    for x in a:
        p.append(p[-1] + x)
    if drop_zero:
        return p[1:]
    else:
        return p


def prefix_mins(a, drop_zero=False):
    p = [float('inf')]
    for x in a:
        p.append(min(p[-1], x))
    if drop_zero:
        return p[1:]
    else:
        return p


class DSU:

    # Disjoint Set Union (Union-Find) Data Structure
    def __init__(self, nodes):
        # Parents
        self.p = [i for i in range(nodes)]
        # Ranks
        self.r = [0 for i in range(nodes)]
        # Sizes
        self.s = [1 for i in range(nodes)]

    def get(self, u):
        # Recursive Returns the identifier of the set that contains u, includes path compression
        if u != self.p[u]:
            self.p[u] = self.get(self.p[u])
        return self.p[u]

    def union(self, u, v):
        # Unites the sets with identifiers u and v
        u = self.get(u)
        v = self.get(v)
        if u != v:
            if self.r[u] > self.r[v]:
                u, v = v, u
            self.p[u] = v
            if self.r[u] == self.r[v]:
                self.r[v] += 1
            self.s[v] += self.s[u]

    def get_size(self, u):
        u = self.get(u)
        return self.s[u]


def solve_b():
    n = get_int()
    p = get_ints()
    dsu = DSU(n)
    for i, x in enumerate(p):
        dsu.union(i, x - 1)
    return [dsu.get_size(i) for i in range(n)]


t = get_int()
for _ in range(t):
    print(*solve_b())
