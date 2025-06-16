#!/usr/bin/env python3


n , m = map(int,input().split())
g = [[] for i in range(n + 1 )]

e = 0
vx = 0

for i in range(m):
    a , b = map(int,input().split())
    g[a].append(b)
    g[b].append(a)

vis = [False for i in range(n + 1 )]

def dfs(node):
    global vx , e
    stack = [node]
    while(stack):
        node = stack.pop()
        if not vis[node]:
            vx +=1
            vis[node] = True
            for j in g[node]:
                e +=1
                stack.append(j)

ans = 'YES'
for i in range(1 , n + 1):
    if not vis[i]:
        e = vx = 0
        dfs(i)
        e //=2
        if e != vx*(vx - 1)//2:
            ans = 'NO'

print(ans)
