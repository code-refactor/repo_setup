#!/usr/bin/env python3

from sys import stdin


class order_tree:
    def __init__(self, n):
        self.tree, self.n = [[0, 0] for _ in range(n << 1)], n

    # get interval[l,r)
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

        # set new value
        self.tree[ix][col] += val

        # move up
        while ix > 1:
            self.tree[ix >> 1][col] = self.tree[ix][col] + self.tree[ix ^ 1][col]
            ix >>= 1


def fast3():
    import os, sys, atexit
    from io import BytesIO
    sys.stdout = BytesIO()
    _write = sys.stdout.write
    sys.stdout.write = lambda s: _write(s.encode())
    atexit.register(lambda: os.write(1, sys.stdout.getvalue()))
    return BytesIO(os.read(0, os.fstat(0).st_size)).readline


input = fast3()
n, a = int(input()), [int(x) for x in input().split()]
tree, ans = order_tree(n), 0
mem = {i: j for j, i in enumerate(sorted(a))}

for i in range(n - 1, -1, -1):
    cur = mem[a[i]]
    ans += tree.query(cur, 1)
    tree.update(cur, 1, 0)
    tree.update(cur, tree.query(cur, 0), 1)

print(ans)
