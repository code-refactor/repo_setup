#!/usr/bin/env python3

def solve():
    n = int(input())
    
    # The algorithm constructs a permutation that maximizes XOR sum
    # The maximum beauty is n*(n+1)
    print(n * (n + 1))
    
    # Create the optimal permutation using bit manipulation approach
    s = n + 1
    lst = []
    new = list(range(n + 1))[::-1]  # [n, n-1, n-2, ..., 1, 0]
    k = 2**20  # Large power of 2
    
    while s:
        while k >= 2 * s:
            k //= 2
        lst = new[n + 1 - s:n + 1 + s - k] + lst
        s = k - s
    
    # Output the permutation on one line, space-separated
    print(' '.join(map(str, lst)))

solve()





