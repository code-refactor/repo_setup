#!/usr/bin/env python3

from library import read_ints, init_dp_2d

def update(tree, pos, diff, si):
    pos += si - 1
    while pos:
        tree[pos] += diff
        pos >>= 1

def query(tree, l, r, si):
    ans, l, r = 0, l + si - 1, r + si - 1
    while l < r:
        if l & 1:
            ans += tree[l]
            l += 1
        if not r & 1:
            ans += tree[r]
            r -= 1
        l, r = l >> 1, r >> 1
    return ans + (0 if l != r else tree[l])

n, k = read_ints()
arr = [int(input()) for _ in range(n)]
si = 1 << (n.bit_length() - (not n & n - 1))
dp = init_dp_2d(k + 1, n)
dp[0] = [1] * n

for i in range(1, k + 1):
    tree = [0] * (si << 1)
    for j in range(n):
        dp[i][j] = query(tree, 1, arr[j], si)
        update(tree, arr[j], dp[i - 1][j], si)

print(sum(dp[-1]))