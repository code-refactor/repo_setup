#!/usr/bin/env python3

from library import parse_int, parse_ints

def solve():
    n = parse_int()
    d = {}
    
    for _ in range(n-1):
        u, v = parse_ints()
        min_ = min(u, v)
        max_ = max(u, v)
        
        if max_ != n:
            return False, None
        
        if min_ not in d:
            d[min_] = 0
        d[min_] += 1
    
    if sum(list(d.values())) + 1 != n:
        return False, None
        
    edge = [] 
    used = {i:False for i in range(1, n+1)}
    
    for k in sorted(list(d.keys())):
        used[k] = True
        mid = [n]  # Start with node n
        
        for i in range(k-1, 0, -1):  # k-1->1
            if len(mid) == d[k]:
                break
                
            if not used[i]:
                used[i] = True
                mid.append(i)
                
        if len(mid) < d[k]:
            return False, None
        
        mid.append(k)
        
        for u, v in zip(mid[:-1], mid[1:]):
            edge.append([u, v])
    
    return True, edge        
            
ans, arr = solve()

if not ans:
    print('NO')
else:
    print('YES')
    for u, v in arr:
        print(f"{u} {v}")


    