#!/usr/bin/env python3

import sys
sys.path.append('..')

from collections import UserDict

class Tree(UserDict):
    def __init__(self, g):
        super().__init__()
        for name, value in enumerate(g, 1):
            self[value] = name

    def __setitem__(self, name, value):
        if name in self:
            if value is not None:
                self[name].add(value)
                self[value] = None
        else:
            if value is None:
                super().__setitem__(name, set())
            else:
                super().__setitem__(name, {value})
                self[value] = None

if __name__ == '__main__':
    n = int(input())
    
    tree = Tree(int(i) for i in input().split())
    colors = [int(i) for i in input().split()]
    t = [()] * n

    def dfs(v):
        stack = [v]
        visited = set()

        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                stack.append(v)
                stack.extend(tree[v])
            else:
                t[v] = (1, colors[v])
                for u in tree[v]:
                    t[v] = (
                        (t[v][0] * t[u][1] + t[v][0] * t[u][0] * (not colors[u])) % (10**9 + 7),
                        (t[v][1] * t[u][1] + t[v][0] * t[u][1] * (not colors[v])
                                           + t[v][1] * t[u][0] * (not colors[u])) % (10**9 + 7)
                    )

                
    dfs(0)

    print(t[0][1])



    




# Made By Mostafa_Khaled