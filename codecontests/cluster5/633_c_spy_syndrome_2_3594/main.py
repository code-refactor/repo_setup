#!/usr/bin/env python3

def solve():
    n = int(input())
    t = input().strip()[::-1]  # Reverse the cipher text
    m = int(input())
    
    # Build dictionary: lowercase -> original case
    d = {}
    for _ in range(m):
        word = input().strip()
        d[word.lower()] = word
    
    # Get sorted unique word lengths for optimization
    l = sorted(set(map(len, d)))
    
    # Backtracking algorithm (original working logic)
    k, s = 0, []
    while n:
        k -= 1
        if len(l) + k < 0: 
            k, n = s.pop()
        elif n >= l[k] and t[n - l[k]:n].lower() in d:
            s.append((k, n))
            n -= l[k]
            k = 0
    
    # Reconstruct the result in correct order
    result = []
    for i, end_pos in s:
        start_pos = end_pos - l[i]
        substring = t[start_pos:end_pos].lower()
        result.append(d[substring])
    
    print(' '.join(result))

solve()