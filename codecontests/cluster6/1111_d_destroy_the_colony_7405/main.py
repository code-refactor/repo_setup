#!/usr/bin/env python3

from library import Combinatorics, MOD, FastIO

s = FastIO.read_string()
n = len(s)
buc = [0] * 101
comb = Combinatorics(n, MOD)
dp = [0] * (n + 1)
ans = [[0] * 55 for _ in range(55)]


def find(c):
    if 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 26
    else:
        return ord(c) - ord('a')


def add(a, b):
    return (a + b) % MOD


def sub(a, b):
    return (a - b) % MOD


for i in s:
    buc[find(i)] += 1

num = pow(comb.fact[n // 2], 2, MOD)
for i in range(0, 52):
    num = (num * comb.inv_fact[buc[i]]) % MOD

dp[0] = 1

for i in range(0, 52):
    if not buc[i]:
        continue
    for j in range(n, buc[i] - 1, -1):
        dp[j] = add(dp[j], dp[j - buc[i]])

for i in range(52):
    ans[i][i] = dp[n // 2]

for i in range(52):
    if not buc[i]:
        continue
    temp_dp = dp.copy()
    for k in range(buc[i], n + 1):
        temp_dp[k] = sub(temp_dp[k], temp_dp[k - buc[i]])

    for j in range(i + 1, 52):
        if not buc[j]:
            continue
        for k in range(buc[j], n + 1):
            temp_dp[k] = sub(temp_dp[k], temp_dp[k - buc[j]])

        ans[i][j] = (2 * temp_dp[n // 2]) % MOD

        for k in range(n, buc[j] - 1, -1):
            temp_dp[k] = add(temp_dp[k], temp_dp[k - buc[j]])

q = FastIO.read_int()
for _ in range(q):
    x, y = FastIO.read_ints()
    l, r = find(s[x - 1]), find(s[y - 1])
    if l > r:
        l, r = r, l
    print(num * ans[l][r] % MOD)
