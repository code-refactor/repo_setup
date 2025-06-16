#!/usr/bin/env python3

import sys
input = sys.stdin.readline

############ ---- Input Functions ---- ############
def inp():
    return(int(input()))
def inlt():
    return(list(map(int,input().split())))
def insr():
    s = input().strip()
    return(list(s[:len(s)]))
def invr():
    return(map(int,input().split()))



def from_file(f):
    return f.readline


def build_graph(n, A, reversed=False):
    edges = [[] for _ in range(n)]
    for i, j in A:
        i -= 1
        j -= 1
        if reversed:
            j, i = i, j
        edges[i].append(j)
    return edges


def fill_min(s, edges, visited_dfs, visited, container):
    visited[s] = True
    visited_dfs.add(s)

    for c in edges[s]:
        if c in visited_dfs:
            # cycle
            return -1
        if not visited[c]:
            res = fill_min(c, edges, visited_dfs, visited, container)
            if res == -1:
                return -1
        container[s] = min(container[s], container[c])
    visited_dfs.remove(s)
    return 0


def dfs(s, edges,  visited, container):

    stack = [s]

    colors = {s: 0}

    while stack:
        v = stack.pop()
        if colors[v] == 0:
            colors[v] = 1
            stack.append(v)
        else:
            # all children are visited
            tmp = [container[c] for c in edges[v]]
            if tmp:
                container[v] = min(min(tmp), container[v])
            colors[v] = 2 # finished
            visited[v] = True

        for c in edges[v]:
            if visited[c]:
                continue
            if c not in colors:
                colors[c] = 0 # white
                stack.append(c)
            elif colors[c] == 1:
                # grey
                return -1
    return 0





def iterate_topologically(n, edges, container):
    visited = [False] * n

    for s in range(n):
        if not visited[s]:
            # visited_dfs = set()
            # res = fill_min(s, edges, visited_dfs, visited, container)
            res = dfs(s, edges, visited, container)
            if res == -1:
                return -1
    return 0


def solve(n, A):
    edges = build_graph(n, A, False)
    container_forward = list(range(n))
    container_backward = list(range(n))

    res = iterate_topologically(n, edges, container_forward)
    if res == -1:
        return None

    edges = build_graph(n, A, True)

    iterate_topologically(n, edges, container_backward)
    container = [min(i,j) for i,j in zip(container_forward, container_backward)]

    res = sum((1 if container[i] == i else 0 for i in range(n)))

    s = "".join(["A" if container[i] == i else "E" for i in range(n)])

    return res, s



# with open('5.txt') as f:
#     input = from_file(f)
n, m = invr()
A = []
for _ in range(m):
    i, j = invr()
    A.append((i, j))

result = solve(n, A)
if not result:
    print (-1)
else:
    print(f"{result[0]}")
    print(f"{result[1]}")
