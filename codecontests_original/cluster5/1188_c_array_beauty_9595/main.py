#!/usr/bin/env python3

from collections import defaultdict
import sys
input = sys.stdin.readline
'''
for CASES in range(int(input())):
n, m = map(int, input().split())
n = int(input())
A = list(map(int, input().split()))
S = input().strip()
sys.stdout.write(" ".join(map(str,ans))+"\n")
'''
inf = 100000000000000000  # 1e17
mod = 998244353

n, m = map(int, input().split())
A = [0] + sorted(list(map(int, input().split())))

ans = 0

f = [[0] * (n + 10) for _ in range(m + 10)]

for x in range(1,(A[n] - A[1]) // (m - 1) + 1):
    for i in range(1, n + 1):
        f[1][i] = 1
    for i in range(2, m + 1):
        sum = 0
        pre = 1
        for j in range(1, n + 1):
            while pre <= n and A[pre] + x <= A[j]:
                sum += f[i - 1][pre]
                sum %= mod
                pre += 1
            f[i][j] = sum
    for i in range(1, n + 1):
        ans += f[m][i]
        ans %= mod
print(ans)


# the end
