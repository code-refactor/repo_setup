#!/usr/bin/env python3

#!/usr/bin/env python
import os
import sys
from io import BytesIO, IOBase


def main():
    print("500")
    cnt = 500
    x = int(input())
    if x % 4 == 3:
        print(str(x) + " + " + str(x))
        print(str(2 * x) + " + " + str(x))
        cnt -= 2
        x *= 3
    xCpy = x
    bigX = x
    while xCpy != 1:
        print(str(bigX) + " + " + str(bigX))
        cnt -= 1
        xCpy //= 2
        bigX *= 2
    print(str(bigX) + " + " + str(x))
    ans1 = bigX + x
    print(str(bigX) + " ^ " + str(x))
    ans2 = bigX ^ x
    print(str(ans1) + " ^ " + str(ans2))
    ans = ans1 ^ ans2
    cnt -= 3
    curX = x
    while ans != 1:
        curX = x
        while curX != 0:
            print(str(curX) + " + " + str(curX))
            cnt -= 1
            curX *= 2
            if curX >= ans:
                print(str(ans) + " ^ " + str(curX))
                cnt -= 1
                curX ^= ans
        ans //= 2
        if x >= ans:
            print(str(x) + " ^ " + str(ans))
            cnt -= 1
            x ^= ans
    while cnt > 0:
        cnt -= 1
        print(str(x) + " + " + str(x))

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

# endregion

if __name__ == "__main__":
    main()