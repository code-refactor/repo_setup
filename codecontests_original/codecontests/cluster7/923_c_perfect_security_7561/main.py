#!/usr/bin/env python3

def add(x):
    global tree
    now = 0
    tree[now][2] += 1
    for i in range(29, -1, -1):
        bit = (x>>i)&1
        if tree[now][bit]==0:
            tree[now][bit]=len(tree)
            tree.append([0, 0, 0])
        now = tree[now][bit]
        tree[now][2] += 1

def find_min(x):
    global tree
    now = ans = 0
    for i in range(29, -1, -1):
        bit = (x>>i)&1
        if tree[now][bit] and tree[tree[now][bit]][2]:
            now = tree[now][bit]
        else:
            now = tree[now][bit^1]
            ans |= (1<<i)
        tree[now][2] -= 1
    return ans

tree = [[0, 0, 0]]
n = int(input())
a = list(map(int, input().split()))
list(map(add, map(int, input().split())))
[print(x, end=' ') for x in list(map(find_min, a))]