#!/usr/bin/env python3

# https://codeforces.com/problemset/problem/575/H

import sys
import math

MOD = 1000000007


def inv(a, b):
    if(a > 1):
        return b-inv(b % a, a)*b//a
    else:
        return 1


def main():
    # sys.stdin = open('E:\\Sublime\\in.txt', 'r')
    # sys.stdout = open('E:\\Sublime\\out.txt', 'w')
    # sys.stderr = open('E:\\Sublime\\err.txt', 'w')

    n = int(sys.stdin.readline().strip())
    # a, b = map(int, sys.stdin.readline().strip().split()[:2])

    # C(n+1, 2n + 2) = (2n+2)! : (n+1)! : n+1!
    # = (n+2)(n+3)...(2n+2) /

    t = 1
    m = 1
    for i in range(1, n + 2):
        t = (t * (n + i + 1)) % MOD
        m = (m * i) % MOD
    print(t * inv(m, MOD) % MOD - 1)


if __name__ == '__main__':
    main()

# hajj
#  　　　　　　 ＿＿
# 　　　　　／＞　　フ
# 　　　　　| 　_　 _ l
# 　 　　　／` ミ＿xノ
# 　　 　 /　　　 　 |
# 　　　 /　 ヽ　　 ﾉ
# 　 　 │　　|　|　|
# 　／￣|　　 |　|　|
# 　| (￣ヽ＿_ヽ_)__)
# 　＼二つ
