#!/usr/bin/env python3

import math 

n = int(input())
k, epsilon = list(map(int, input().split(" ")))
x0, y0 = list(map(int, input().split(" ")))
epsilon /= 1000.0

l = []
for i in range(n):
    l.append(list(map(int, input().split(" "))))
    
d = sorted([(p[0] - x0) ** 2 + (p[1] - y0) ** 2 for p in l])

rmin = 0
rmax = math.sqrt(d[k - 1])

while(1):
    if(rmax - rmin < 10e-9):
        print((rmin + rmax)/2) 
        break
    
    r = (rmin + rmax)/2
    p = [math.exp(1 - i/(r**2)) if i > r**2 else 1.0 for i in d]
    
    dp = [[0] * (n + 1) for i in range(n + 1)]
    
    dp[0][0] = 1
    for i in range(1, n + 1):
        for j in range(i + 1):
            if(j > 0):
                dp[i][j] = p[i - 1] * dp[i - 1][j - 1]
            if(i != j):
                dp[i][j] += (1 - p[i - 1]) * dp[i - 1][j]
                
    s = 0
    for j in range(k, n + 1):
        s += dp[n][j]
    
    if(s > 1 - epsilon):
        rmax = r
    else:
        rmin = r

   
    
    
    
    