#!/usr/bin/env python3

import sys
import os

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def query(a):
    os.write(1,b"%d\n" % a)
    return str(os.read(0,100))

def solve(case):
    cnt = 0
    primes = [2,3,5,7]
    div = []
    for i in range(len(primes)):
        ans = query(primes[i])
        if('yes' in ans):
            div.append(primes[i])
            cnt+=1

    if(cnt == 0):
        print('prime')
    else:
        if(len(div) == 1):
            i = div[0]
            x = 2
            cnt = 0
            while((i**x)<101):
                if('yes' in query(i**x)):
                    cnt+=1
                    break
                x+=1
            new = []
            for i in range(10,50):
                if(is_prime(i)):
                    new.append(i)
            for i in new:
                if(div[0]*i>100):
                    break
                if('yes' in query(i)):
                    cnt+=1
            if(cnt == 0):
                print('prime')
            else:
                print('composite')
        else:
            print('composite')

solve(1)