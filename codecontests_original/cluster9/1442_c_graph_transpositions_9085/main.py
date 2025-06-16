#!/usr/bin/env python3

# region fastio  # from https://codeforces.com/contest/1333/submission/75948789
import sys, io, os

BUFSIZE = 8192


class FastIO(io.IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = io.BytesIO()
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


class IOWrapper(io.IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


def print(*args, **kwargs):
    """Prints the values to a stream, or to sys.stdout by default."""
    sep, file = kwargs.pop("sep", " "), kwargs.pop("file", sys.stdout)
    at_start = True
    for x in args:
        if not at_start:
            file.write(sep)
        file.write(str(x))
        at_start = False
    file.write(kwargs.pop("end", "\n"))
    if kwargs.pop("flush", False):
        file.flush()


sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
input = lambda: sys.stdin.readline().rstrip("\r\n")
#endregion


from heapq import heappush, heappop
mod = 998244353
N, M = map(int, input().split())
E1 = [[] for _ in range(N)]
E2 = [[] for _ in range(N)]
for _ in range(M):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    E1[u].append(v)
    E2[v].append(u)



# コスト、転倒回数(5bit)、ノード(18bit)

mask1 = (1<<23) - 1
mask2 = (1<<18) - 1

# ダイクストラ法
inf = 1<<62
dist = [inf] * (1<<23)
start = 0
dist[start] = 0
q = [start]
while q:
    v = heappop(q)
    dist_v = v >> 23
    v &= mask1
    n_trans = v >> 18
    v_node = v & mask2
    if v_node == N-1:
        print(dist_v % mod)
        exit()
    if n_trans > 20:
        break
    if dist[v] != dist_v:
        continue

    for u_node in (E1[v_node] if n_trans&1==0 else E2[v_node]):
        u = n_trans<<18 | u_node
        dist_u = dist_v + 1
        if dist_u < dist[u]:
            dist[u] = dist_u
            heappush(q, dist_u<<23 | u)
    u = n_trans+1<<18 | v_node
    dist_u = dist_v + (1<<n_trans)
    if dist_u < dist[u]:
        dist[u] = dist_u
        heappush(q, dist_u<<23 | u)

#################################

# 転倒回数、移動回数(18bit)、ノード(19bit)

mask1 = (1<<37) - 1
mask2 = (1<<19) - 1
mask3 = (1<<18)-1
REV = 1<<18

dist = [inf] * (1<<19)
start = 0
dist[start] = 0
q = [start]
while q:
    v = heappop(q)
    dist_v = v >> 19
    n_trans = dist_v >> 18
    v &= mask2
    v_node = v & mask3
    if v_node == N-1:
        ans = pow(2, n_trans, mod) - 1 + (dist_v&mask3)
        print(ans)
        exit()
    rev = v & REV
    if dist[v] != dist_v:
        continue
    for u_node in (E1[v_node] if n_trans&1==0 else E2[v_node]):
        u = rev | u_node
        dist_u = dist_v + 1
        if dist_u < dist[u]:
            dist[u] = dist_u
            heappush(q, dist_u<<19 | u)
    u = v ^ REV
    dist_u = dist_v + (1<<18)
    if dist_u < dist[u]:
        dist[u] = dist_u
        heappush(q, dist_u<<19 | u)

assert False
