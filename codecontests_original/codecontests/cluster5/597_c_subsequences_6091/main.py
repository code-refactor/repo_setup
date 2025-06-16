#!/usr/bin/env python3

# by the authority of GOD     author: manhar singh sachdev #

import os,sys
from io import BytesIO, IOBase

def update(tree,pos,diff,si):
    pos += si-1
    while pos:
        tree[pos] += diff
        pos >>= 1

def query(tree,l,r,si):
    ans,l,r = 0,l+si-1,r+si-1
    while l < r:
        if l&1:
            ans += tree[l]
            l += 1
        if not r&1:
            ans += tree[r]
            r -= 1
        l,r = l>>1,r>>1
    return ans+(0 if l!=r else tree[l])

def main():
    n,k = map(int,input().split())
    arr = [int(input()) for _ in range(n)]
    si = 1<<(n.bit_length()-(not n&n-1))
    dp = [[0]*n for _ in range(k+1)]
    dp[0] = [1]*n
    for i in range(1,k+1):
        tree = [0]*(si<<1)
        for j in range(n):
            dp[i][j] = query(tree,1,arr[j],si)
            update(tree,arr[j],dp[i-1][j],si)
    print(sum(dp[-1]))

#Fast IO Region
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

if __name__ == '__main__':
    main()