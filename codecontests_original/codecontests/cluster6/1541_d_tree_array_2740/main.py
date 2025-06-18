#!/usr/bin/env python3

from functools import lru_cache
from collections import deque

M = 10 ** 9 + 7


@lru_cache(None)
def inv(x):
    return pow(x, M - 2, M)


@lru_cache(None)
def dp(u, v):
    # u before v
    if u == 0:
        return 0
    if v == 0:
        return 1
    return (dp(u - 1, v) * inv(2) + dp(u, v - 1) * inv(2)) % M


def calc(n, link, start):
    res = 0
    for u in range(1, n + 1):
        for v in range(u + 1, n + 1):
            lca = (link[start][u] + link[start][v] - link[u][v]) // 2
            res += dp(link[start][u] - lca, link[start][v] - lca)
            res %= M
    return res


def main():
    n = int(input())
    graph = [[] for i in range(n + 1)]
    ans = 0
    for _ in range(n - 1):
        u, v = [int(word) for word in input().split()]
        graph[u].append(v)
        graph[v].append(u)
    link = [[-1 for j in range(n + 1)] for i in range(n + 1)]
    for i in range(1, n + 1):
        link[i][i] = 0
        q = deque()
        q.append(i)
        while len(q) != 0:
            u = q.popleft()
            for v in graph[u]:
                if link[i][v] >= 0:
                    continue
                link[i][v] = link[i][u] + 1
                q.append(v)
    for root in range(1, n + 1):
        ans += calc(n, link, start=root)
        ans %= M
    ans *= inv(n)
    ans %= M
    print(ans)


if __name__ == "__main__":
    main()
