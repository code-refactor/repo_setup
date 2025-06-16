#!/usr/bin/env python3

# from __future__ import division, print_function

import sys
import os
from io import BytesIO, IOBase


# def inp(): return sys.stdin.readline().rstrip("\r\n") #for fast input



# n = int(os.read(0,100))
# if(n==1):
#     os.write(1,b'! 1')
#     sys.stdout.flush()
# else:
#     per = [0]*n
#     # print('? 2 1')
#     # sys.stdout.flush()
#     a1 = query(1,0)
#     # print('? 1 2')
#     # sys.stdout.flush()
#     a2 = int(query(0,1))
#     if(a2>a1):
#         max = 2
#         per[0] = a2
#     else:
#         max = 1
#         per[1] = a1
#     # print(per)
#     for i in range(3,n+1):
#         # print('? '+str(i)+" "+str(max))
#         # sys.stdout.flush()
#         a1 = int(query(i-1,max-1))
#         # print('? '+str(max)+' '+str(i))
#         # sys.stdout.flush()
#         a2  = int(query(max-1,i-1))
#         if(a1>a2):
#             per[i-1] = a1
#         else:
#             per[max-1] = a2
#             max = i
#         # print(per)
#     per[max-1] = n
#     # print('! ',end="")
#     # print(' '.join(str(per[i]) for i in range(len(per))))
#     # sys.stdout.flush()
#     os.write(1, b'! ')
#     os.write(1, b' '.join(str(x).encode('ascii') for x in per))

def isPrime(n) :
    if (n <= 1) : return False
    if (n <= 3) : return True
    if (n % 2 == 0 or n % 3 == 0) : return False
    i = 5
    while(i * i <= n) :
        if (n % i == 0 or n % (i + 2) == 0) :
            return False
        i = i + 6
    return True

def query(a):
    # print(1)
    os.write(1,b"%d\n" % a)
    return str(os.read(0,100))

def solve(case):
    cnt = 0
    primes = [2,3,5,7]
    div = []
    for i in range(len(primes)):
        # print(primes[i])
        # sys.stdout.flush()
        # ans = inp()
        ans = query(primes[i])
        # print(ans)
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
                # print(i**x)
                # sys.stdout.flush()
                if('yes' in query(i**x)):
                    cnt+=1
                    break
                x+=1
            new = []
            for i in range(10,50):
                if(isPrime(i)):
                    new.append(i)
            for i in new:
                if(div[0]*i>100):
                    break
                # print(i)
                # sys.stdout.flush()
                if('yes' in query(i)):
                    cnt+=1
            if(cnt == 0):
                print('prime')
            else:
                print('composite')
        else:
            print('composite')




solve(1)
