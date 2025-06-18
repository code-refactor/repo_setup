#!/usr/bin/env python3


import atexit
import io
import sys

# IO Buffering
_INPUT_LINES = sys.stdin.read().splitlines()
input = iter(_INPUT_LINES).__next__
_OUTPUT_BUFFER = io.StringIO()
sys.stdout = _OUTPUT_BUFFER

@atexit.register
def write():
    sys.__stdout__.write(_OUTPUT_BUFFER.getvalue())
    
    
def main():
    n = int(input())
    a = sorted(int(x) for x in input().split())

    factorial = [1] * n
    # perm_n[a] = P(n, a) = n!/(n-a)!
    perm_n = [1] * n
    for i in range(1, n):
        factorial[i] = factorial[i - 1] * i % 1000000007
        perm_n[i] = perm_n[i - 1] * (n - i + 1) % 1000000007
    
    ans = 0
    l = 0
    for i in range(n):
        if a[i] == a[-1]: 
            break
        if a[i] > a[i - 1]:
            l = i
        ans += a[i] * perm_n[l] * factorial[n - l - 1]

    print(ans % 1000000007)
            
        
if __name__ == '__main__':
    main()