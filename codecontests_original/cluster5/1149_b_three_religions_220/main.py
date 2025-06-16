#!/usr/bin/env python3

n, q = map(int, input().split())
s = '!' + input()

nxt = [[n + 1] * (n + 2) for _ in range(26)]
for i in range(n - 1, -1, -1):
    c = ord(s[i + 1]) - 97
    for j in range(26):
        nxt[j][i] = nxt[j][i + 1]
    nxt[c][i] = i + 1

w = [[-1], [-1], [-1]]
idx = lambda i, j, k: i * 65536 + j * 256 + k
dp = [0] * (256 * 256 * 256)
def calc(fix=None):
    r = list(map(range, (len(w[0]), len(w[1]), len(w[2]))))
    if fix is not None: r[fix] = range(len(w[fix]) - 1, len(w[fix]))
    for i in r[0]:
        for j in r[1]:
            for k in r[2]:
                dp[idx(i, j, k)] = min(nxt[w[0][i]][dp[idx(i - 1, j, k)]] if i else n + 1,
                                       nxt[w[1][j]][dp[idx(i, j - 1, k)]] if j else n + 1,
                                       nxt[w[2][k]][dp[idx(i, j, k - 1)]] if k else n + 1)
                if i == j == k == 0: dp[idx(i, j, k)] = 0

out = []
for _ in range(q):
    t, *r = input().split()
    if t == '+':
        i, c = int(r[0]) - 1, ord(r[1]) - 97
        w[i].append(c)
        calc(i)
    else:
        i = int(r[0]) - 1
        w[i].pop()
    req = dp[idx(len(w[0]) - 1, len(w[1]) - 1, len(w[2]) - 1)]
    out.append('YES' if req <= n else 'NO')

print(*out, sep='\n')