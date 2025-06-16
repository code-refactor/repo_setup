#!/usr/bin/env python3

from library import read_ints

n, x, y = read_ints()
lu=0
ld=0
ru=0
rd=0
u=0
d=0
l=0
r=0

for i in range(n):
    a, b = read_ints()
    if(a<x and b<y):
        ld+=1
    elif(a<x and b>y):
        lu+=1
    elif(a==x and b!=y):
        if(b>y):
            u+=1
        else:
            d+=1
    elif(a>x and b<y):
        rd+=1
    elif(a>x and b>y):
        ru+=1
    elif(a!=x and b==y):
        if(a<x):
            l+=1
        else:
            r+=1

l1=[]
#print(lu,ru,ld,rd,u,d,l,r)
l1.append(lu+ru+u)
l1.append(lu+ld+l)
l1.append(ru+rd+r)
l1.append(ld+rd+d)
ans=max(l1)
ind=l1.index(max(l1))
print(ans)
if(ind==0):
    print(x,y+1)
elif(ind==1):
    print(x-1,y)
elif(ind==2):
    print(x+1,y)
else:
    print(x,y-1)
    
        
        
        