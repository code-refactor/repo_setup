#!/usr/bin/env python3

for _ in range(int(input())):
    n=int(input())
    i=1
    c=2
    l=[]
    y=n
    while(i<=2):
        if n%c==0:
            n=n//c
            i=i+1
            l.append(c)
        if c>=y**0.5:
            break
        c=c+1
    if l==[] or len(l)==1:
        print("NO")
    elif y%(l[0]*l[1])==0:
        x=y//(l[0]*l[1])
        if x not in l and x!=1:
            print("YES")
            l.append(x)
            for i in range(len(l)):
                if i==len(l)-1:
                    print(l[i])
                else:
                    print(l[i],end=" ")
        else:
            print("NO")
    else:
        print("NO")