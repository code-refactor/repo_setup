#!/usr/bin/env python3

# 

def solve():
    n = int(input())
    d = {}
    
    for _ in range(n-1):
        u, v = map(int, input().split())
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
        mid     = [n]
        
        for i in range(k-1, 0, -1): # k-1->1
            
            if len(mid) == d[k]:
                break
                
            if used[i] == False:
                used[i] = True
                mid.append(i)
                
        if len(mid) < d[k]:
            return False, None
        
        mid.append(k)
        
        for  u, v in zip(mid[:-1], mid[1:]):
            edge.append([u, v])
    
    return True, edge        
            
ans, arr = solve()

if ans == False:
    print('NO')
else:
    print('YES')
    for u, v in arr:
        print(str(u)+' '+str(v))

#4
#3 4
#1 4
#3 4    
    