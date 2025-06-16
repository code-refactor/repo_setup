#!/usr/bin/env python3

t=int(input())
for i in range(t):
    n=int(input())
    if n==1:
        print(0)
    else:
        if n%3!=0:
            print(-1)
        else:
            threes=0
            twos=0
            while n%3==0:
                threes+=1
                n=n//3
            while n%2==0:
                twos+=1
                n=n//2
            if n!=1 or twos>threes:
                print(-1)
            else:
                print(2*threes-twos)
