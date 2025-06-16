#!/usr/bin/env python3

from sys import stdin, stdout
import math,sys,heapq
from itertools import permutations, combinations
from collections import defaultdict,deque,OrderedDict
from os import path
import random
import bisect as bi
def yes():print('YES')
def no():print('NO')
if (path.exists('input.txt')): 
    #------------------Sublime--------------------------------------#
    sys.stdin=open('input.txt','r');sys.stdout=open('output.txt','w');
    def I():return (int(input()))
    def In():return(map(int,input().split()))
else:
    #------------------PYPY FAst I/o--------------------------------#
    def I():return (int(stdin.readline()))
    def In():return(map(int,stdin.readline().split()))
#sys.setrecursionlimit(1500)
def dict(a):
    d={} 
    for x in a:
        if d.get(x,-1)!=-1:
            d[x]+=1
        else:
            d[x]=1
    return d
def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bi.bisect_left(a, x)
    if i != len(a):
        return i
    else:            
        return -1
        
def main():
    try:
        n=I()
        l=list(In())
        if n&1!=1:
            su=l[0]
            for i in range(1,n):
                su^=l[i]
            if su!=0:
                no()
                return
        yes()
        z=(n-1)//2
        print(2*z)
        for i in range(z):
            s=str(2*i+1)+' '+str(2*i+2)+' '+str(n)
            stdout.write(s+'\n')
        for i in range(z):
            s=str(2*i+1)+' '+str(2*i+2)+' '+str(n)
            stdout.write(s+'\n')
    except:
        pass
        
M = 998244353
P = 1000000007
 
if __name__ == '__main__':
    #for _ in range(I()):main()
    for _ in range(1):main()