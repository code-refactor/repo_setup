#!/usr/bin/env python3

def arr_inp():
    return [int(x) for x in stdin.readline().split()]


class graph:
    # initialize graph
    def __init__(self, gdict=None):
        if gdict is None:
            gdict = defaultdict(list)
        self.gdict = gdict

    # get edges
    def edges(self):
        return self.find_edges()

    # find edges
    def find_edges(self):
        edges = []
        for node in self.gdict:
            for nxNode in self.gdict[node]:
                if {nxNode, node} not in edges:
                    edges.append({node, nxNode})
        return edges

    # Get verticies
    def get_vertices(self):
        return list(self.gdict.keys())

    # add vertix
    def add_vertix(self, node):
        self.gdict[node] = []

    # add edge
    def add_edge(self, node1, node2):
        self.gdict[node1].append(node2)
        self.gdict[node2].append(node1)

    def dfsUtil(self, v, par):

        self.visit[v] = 1

        for i in self.gdict[v]:
            if self.visit[i] == 0:
                self.dfsUtil(i, v)
                self.topsort += 1
            elif i != par and v != par:
                self.topsort += 1
                self.flag = 1

    # dfs for graph
    def dfs(self):
        self.visit, self.cnt, self.topsort, self.flag = defaultdict(int), 0, 0, 0

        for i in self.get_vertices():
            if self.visit[i] == 0:
                self.dfsUtil(i, i)

                if self.topsort & 1 and self.topsort >= 3 and self.flag:
                    self.cnt += 1
                self.flag = 0
                self.topsort = 0
        return self.cnt


from collections import defaultdict
from sys import stdin

n, m = arr_inp()
student = graph()
for i in range(m):
    a, b = arr_inp()
    student.add_edge(a, b)

ans = student.dfs()
print(ans + 1 if (n - ans) & 1 else ans)
