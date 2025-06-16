#!/usr/bin/env python3

class BIT:
    def __init__(self, n):
        self.tree = [[0, 0] for _ in range(n << 1)]
        self.n = n

    def query(self, r, col):
        res = 0
        l = self.n
        r += self.n
        while l < r:
            if l & 1:
                res += self.tree[l][col]
                l += 1
            if r & 1:
                r -= 1
                res += self.tree[r][col]
            l >>= 1
            r >>= 1
        return res

    def update(self, ix, val, col):
        ix += self.n
        self.tree[ix][col] += val
        while ix > 1:
            self.tree[ix >> 1][col] = self.tree[ix][col] + self.tree[ix ^ 1][col]
            ix >>= 1

n = int(input())
a = list(map(int, input().split()))
tree = BIT(n)
mem = {v: i for i, v in enumerate(sorted(a))}
ans = 0

for i in range(n - 1, -1, -1):
    cur = mem[a[i]]
    ans += tree.query(cur, 1)
    tree.update(cur, 1, 0)
    tree.update(cur, tree.query(cur, 0), 1)

print(ans)
