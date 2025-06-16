#!/usr/bin/env python3

def main():
    n, m = map(int, input().split())
    n += 1
    cluster, dest, ab = list(range(n)), [0] * n, [[] for _ in range(n)]

    def root(x):
        if x != cluster[x]:
            cluster[x] = x = root(cluster[x])
        return x

    for _ in range(m):
        a, b = map(int, input().split())
        ab[a].append(b)
        dest[b] += 1
        cluster[root(a)] = root(b)
    pool = [a for a, f in enumerate(dest) if not f]
    for a in pool:
        for b in ab[a]:
            dest[b] -= 1
            if not dest[b]:
                pool.append(b)
    ab = [True] * n
    for a, f in enumerate(dest):
        if f:
            ab[root(a)] = False
    print(n - sum(f and a == c for a, c, f in zip(range(n), cluster, ab)))


if __name__ == '__main__':
    from sys import setrecursionlimit

    setrecursionlimit(100500)
    main()
