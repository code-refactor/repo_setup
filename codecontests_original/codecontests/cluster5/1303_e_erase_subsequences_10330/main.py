#!/usr/bin/env python3

# by the authority of GOD     author: manhar singh sachdev #

import os,sys
from io import BytesIO,IOBase
from math import inf,isinf

def solve(s,t):
    if len(t) == 1:
        if s.count(t[0]):
            return 'YES'
        return 'NO'
    for i in range(1,len(t)):
        dp = [[-inf]*(i+1) for _ in range(len(s)+1)]
        dp[0][0] = 0
        for j in range(len(s)):
            dp[j+1] = dp[j][:]
            for k in range(i+1):
                if k != i and s[j] == t[k]:
                    dp[j+1][k+1] = max(dp[j+1][k+1],dp[j][k])
                if dp[j][k]+i != len(t) and not isinf(dp[j][k]) and s[j] == t[dp[j][k]+i]:
                    dp[j+1][k] = max(dp[j+1][k],dp[j][k]+1)
        # print(*dp,sep='\n')
        # print('-----')
        for l in range(len(s)+1):
            if dp[l][-1] == len(t)-i:
                return 'YES'
    return 'NO'

def main():
    for _ in range(int(input())):
        s = input().strip()
        t = input().strip()
        print(solve(s,t))

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