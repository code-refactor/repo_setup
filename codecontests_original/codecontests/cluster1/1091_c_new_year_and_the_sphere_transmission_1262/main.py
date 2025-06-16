#!/usr/bin/env python3

n=int(input())
a={1}
for i in range(2,int(n**0.5)+1):
    if n%i==0:
        a.add(i)
        a.add(n//i)
ans=[1]
a=list(a)
for i in a:
    term=n//i
    ans.append((term*(2+(term-1)*i))//2)
ans.sort()
print(*ans)