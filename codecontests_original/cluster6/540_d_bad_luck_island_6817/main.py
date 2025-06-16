#!/usr/bin/env python3

A, B, C = map(lambda x: int(x)+1, input().split())
M = max(max(A, B), C)
p = [[[0] * (M) for i in range(M)] for j in range(M)]

for a in range(M):
    for b in range(M):
        for c in range(M):
            val=0    
            if a == 0 or b == 0:
                val=0
            elif c == 0:
                val=1
            else:
                div = a*b + b*c + c*a
                val = (a*b) / div * p[a][b-1][c] + \
                      (b*c) / div * p[a][b][c-1] + \
                      (a*c) / div * p[a-1][b][c]
            
            p[a][b][c]=val    
            
print(p[A-1][B-1][C-1], p[B-1][C-1][A-1], p[C-1][A-1][B-1])        