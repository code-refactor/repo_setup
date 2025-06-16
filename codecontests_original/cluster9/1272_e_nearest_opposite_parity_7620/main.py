#!/usr/bin/env python3


input()
n=map(int,input().split())
n=list(n)
ans=len(n)*[-1]
a=[]
go=[[] for _ in range(len(n))]
for i,x in enumerate(n):
    for y in (x,-x):
        y+=i
        if y>=0 and y<len(n):
            if x%2!=n[y]%2:
                ans[i]=1
                a.append(i)
            else:
                go[y].append(i)

while len(a)!=0:
    b=[]
    for x in a:
        for y in go[x]:
            if ans[y]==-1:
                ans[y]=ans[x]+1
                b.append(y)
    a=b
for i,x in enumerate(ans):
    ans[i]=str(x)
print(' '.join(ans))