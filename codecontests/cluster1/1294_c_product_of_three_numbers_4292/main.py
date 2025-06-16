#!/usr/bin/env python3

for _ in range(int(input())):
    n = int(input())
    a = 0
    
    # Find first factor a >= 2
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            a = i
            break
    
    if a == 0:
        print("NO")
        continue
    
    remaining = n // a
    b = 0
    
    # Find second factor b >= 2, b != a
    for i in range(2, int(remaining**0.5) + 1):
        if remaining % i == 0 and i != a:
            b = i
            break
    
    if b == 0:
        print("NO")
        continue
    
    c = remaining // b
    
    if c >= 2 and c != a and c != b:
        print("YES")
        print(a, b, c)
    else:
        print("NO")