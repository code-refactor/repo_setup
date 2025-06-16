#!/usr/bin/env python3

from library import gcd
from collections import Counter

def N(): return int(input())
def RL(): return map(int, input().split()) 

for _ in range(N()):
    dic = Counter()
    for _ in range(N()):
        x, y, u, v = RL()
        dx, dy = u - x, v - y 
        if dx == 0:
            dic[(0, 1 if dy > 0 else -1)] += 1
        elif dy == 0:
            dic[(1 if dx > 0 else -1, 0)] += 1
        else:
            t = gcd(abs(dx), abs(dy))
            dic[(dx // t, dy // t)] += 1
    print(sum(dic[(x, y)] * dic[(-x, -y)] for x, y in dic) >> 1)
