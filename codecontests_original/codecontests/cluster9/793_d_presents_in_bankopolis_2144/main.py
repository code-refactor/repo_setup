#!/usr/bin/env python3

import sys
from functools import lru_cache
input = sys.stdin.readline
# sys.setrecursionlimit(2 * 10**6)


def inpl():
    return list(map(int, input().split()))


@lru_cache(maxsize=None)
def recur(v, s, e, k):
    """
    vから初めて[s, e]の都市をk個まわる最小値は？
    """
    if k == 0:
        return 0
    elif k > e - s + 1:
        return INF

    ret = INF
    # print(v, k)
    for nv in edge[v]:
        if not(s <= nv <= e):
            continue

        tmp = [0] * 2
        if v < nv:
            tmp[0] = recur(nv, max(s, v + 1), nv - 1, k - 1)
            tmp[1] = recur(nv, nv + 1, e, k - 1)
        else:
            tmp[0] = recur(nv, s, nv - 1, k - 1)
            tmp[1] = recur(nv, nv + 1, min(v - 1, e), k - 1)
        # print(v, nv, tmp)
        if min(tmp) + cost[(v, nv)] < ret:
            ret = min(tmp) + cost[(v, nv)]
    return ret


def main():
    M = int(input())
    U, V, C = [], [], []
    for _ in range(M):
        u, v, c = inpl()
        U.append(u)
        V.append(v)
        C.append(c)

    for u, v, c in zip(U, V, C):
        if (u, v) in cost:
            cost[(u, v)] = min(cost[(u, v)], c)
        else:
            edge[u].append(v)
            cost[(u, v)] = c

    # print(cost)
    ans = INF
    for v in range(N + 1):
        for nv in edge[v]:
            tmp = [float('inf')] * 2
            if v < nv:
                tmp[0] = recur(nv, nv + 1, N, K - 2)
                tmp[1] = recur(nv, v + 1, nv - 1, K - 2)
            else:
                tmp[0] = recur(nv, 1, nv - 1, K - 2)
                tmp[1] = recur(nv, nv + 1, v - 1, K - 2)
            if min(tmp) + cost[(v, nv)] < ans:
                ans = min(tmp) + cost[(v, nv)]

    if ans == INF:
        print(-1)
    else:
        print(ans)


if __name__ == '__main__':
    INF = float('inf')
    N, K = inpl()
    if K < 2:
        print(0)
        exit()
    edge = [[] for _ in range(N + 1)]
    cost = {}
    main()
