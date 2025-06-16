#!/usr/bin/env python3
from library import read_ints, xor_range

def solve():
    n = int(input())
    xor = 0
    
    for _i in range(n):
        x, m = read_ints()
        # xor_range in library takes (l, r) inclusive, but we need xor from x to x+m-1
        # which is equivalent to xor_range(x, x+m-1)
        # Original code: xor_range(x-1) ^ xor_range(x+m-1) = xor from x to x+m-1
        xor ^= xor_range(x, x + m - 1)
    
    print(["tolik", "bolik"][xor == 0])

if __name__ == '__main__':
    solve()