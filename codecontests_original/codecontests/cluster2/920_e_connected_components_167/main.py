#!/usr/bin/env python3

n,m=map(int,input().split())
non=[{i} for i in range(n)]
for i in range(m):
    u,v=map(int,input().split())
    u,v=u-1,v-1
    non[u].add(v)
    non[v].add(u)
vertex=set(range(n))
ans=[]
while(vertex):
    a=next(iter(vertex))
    vertex.remove(a)
    stk=[a]
    cou=1
    while(stk):
        v=stk.pop()
        s=vertex-non[v]
        cou+=len(s)
        stk.extend(s)
        vertex&=non[v]
    ans.append(cou)
ans.sort()
print(len(ans))
print(" ".join(map(str,ans)))
    