#!/usr/bin/env python3

#import math
#from functools import lru_cache
#import heapq
#from collections import defaultdict
from collections import Counter
#from collections import deque
#from sys import stdout
#from sys import setrecursionlimit
#setrecursionlimit(10**7)
#from bisect import bisect_left
from sys import stdin
input = stdin.readline

INF = 10**9 + 7
MAX = 10**7 + 7
MOD = 10**9 + 7

n, k = [int(x) for x in input().strip().split()]
a = [int(x) for x in input().strip().split()]
c = list(Counter(a).items())
c.sort()
#c.append((0, 0))
s = 0
fi = 0
i = 0
while(i<len(c)):
    s += c[i][1]*n
    #print(i, s)
    if(s>=k):
        fi = i
        k -= (s - c[i][1]*n)
        break
    i+=1
si = 0
i = 0
s = 0
while(i<len(c)):
    s += c[i][1]*c[fi][1]
    #print(i, s)
    if(s>=k):
        si = i
        break
    i+=1
print(c[fi][0], c[si][0])
