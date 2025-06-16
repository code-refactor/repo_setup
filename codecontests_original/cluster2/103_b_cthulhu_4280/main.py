#!/usr/bin/env python3


inp = input().split()

n = int(inp[0])
m = int(inp[1])

def dfs(x):

    visited.add(x)

    for y in e[x]:

        if not y in visited:

            dfs(y)

if n >= 3 and n == m:

    visited = set()

    e = [[] for i in range(n + 1)]
    
    for i in range(m):
    
        x, y = map(int, input().split())
    
        e[x].append(y)
    
        e[y].append(x)

    dfs(1)
 
    print('FHTAGN!' if len(visited) == n else 'NO')
else:
    print('NO')

 
 