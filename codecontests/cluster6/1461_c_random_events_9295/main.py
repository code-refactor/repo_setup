#!/usr/bin/env python3

from library import FastIO

def solve():
    n, m = FastIO.read_ints()
    a = FastIO.read_ints()
    
    j = n - 1
    while j != -1 and a[j] == j + 1:
        j -= 1
    
    if j == -1:
        for _ in range(m):
            FastIO.read_string()
        print(1)
        return
    
    ans = 0
    prob_no_success = 1
    for _ in range(m):
        line = FastIO.read_string().split()
        r, p = int(line[0]), float(line[1])
        
        if r >= j + 1:
            ans += prob_no_success * p
            prob_no_success *= (1 - p)
    
    print(ans)

FastIO.solve_multiple_cases(solve)