#!/usr/bin/env python3

import random
from library import FastIO

N = FastIO.read_int()
prob = [float(x)/100 for x in FastIO.read_string().split()]
prob_sum = []
cur = 0
for i in range(N):
    cur += prob[i]
    prob_sum.append(cur)

def experiment():
    cur_prob = [1.] * N
    cur_exp = 0
    for i in range(200000):

        bp = [prob[i] * cur_prob[i] / (1-cur_prob[i]+1E-100) for i in range(N)]
        mn = max(bp)
        for j in range(N):
            if bp[j] == mn:
                choice = j
        cur_prob[choice] *= 1-prob[choice]
        tp = 1
        for j in range(N):
            tp *= (1-cur_prob[j])
        tp = 1 - tp
        cur_exp += tp

    return cur_exp + 1

ans = experiment()
print(ans)
