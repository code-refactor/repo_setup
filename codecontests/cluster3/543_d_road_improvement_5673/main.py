#!/usr/bin/env python3

from library import read_int, read_ints, setup_io
from functools import reduce
from itertools import accumulate, chain

# Set up fast I/O
input = setup_io()

# Constants
MOD = 10**9 + 7

# Define Graph and RootedTree classes as in the original code
class Graph:
    def __init__(self, n_vertices, edges, directed=True, weighted=False):
        self.n_vertices = n_vertices
        self.edges = edges
        self.directed = directed
        self.weighted = weighted

    @property
    def adj(self):
        try:
            return self._adj
        except AttributeError:
            adj = [[] for _ in range(self.n_vertices)]
            def d_w(e):
                adj[e[0]].append((e[1],e[2]))
            def ud_w(e):
                adj[e[0]].append((e[1],e[2]))
                adj[e[1]].append((e[0],e[2]))
            def d_uw(e):
                adj[e[0]].append(e[1])
            def ud_uw(e):
                adj[e[0]].append(e[1])
                adj[e[1]].append(e[0])
            helper = (ud_uw, d_uw, ud_w, d_w)[self.directed+self.weighted*2]
            for e in self.edges:
                helper(e)
            self._adj = adj
            return adj

class RootedTree(Graph):
    def __init__(self, n_vertices, edges, root_vertex):
        self.root = root_vertex
        super().__init__(n_vertices, edges, False, False)

    @property
    def parent(self):
        try:
            return self._parent
        except AttributeError:
            adj = self.adj
            parent = [None]*self.n_vertices
            parent[self.root] = -1
            stack = [self.root]
            for i in range(self.n_vertices):
                v = stack.pop()
                for u in adj[v]:
                    if parent[u] is None:
                        parent[u] = v
                        stack.append(u)
            self._parent = parent
            return parent

    @property
    def children(self):
        try:
            return self._children
        except AttributeError:
            children = [None]*self.n_vertices
            for v,(l,p) in enumerate(zip(self.adj,self.parent)):
                children[v] = [u for u in l if u != p]
            self._children = children
            return children

    @property
    def dfs_order(self):
        try:
            return self._dfs_order
        except AttributeError:
            order = [None]*self.n_vertices
            children = self.children
            stack = [self.root]
            for i in range(self.n_vertices):
                v = stack.pop()
                order[i] = v
                for u in children[v]:
                    stack.append(u)
            self._dfs_order = order
            return order

# Tree rerooting algorithm with the original implementation
def rerooting(rooted_tree, merge, identity, finalize):
    N = rooted_tree.n_vertices
    parent = rooted_tree.parent
    children = rooted_tree.children
    order = rooted_tree.dfs_order

    # from leaf to parent
    dp_down = [None]*N
    for v in reversed(order[1:]):
        dp_down[v] = finalize(reduce(merge,
            (dp_down[c] for c in children[v]),
            identity))

    # from parent to leaf
    dp_up = [None]*N
    dp_up[0] = identity
    for v in order:
        if len(children[v]) == 0:
            continue
        temp = (dp_up[v],)+tuple(dp_down[u] for u in children[v])+(identity,)
        left = tuple(accumulate(temp,merge))
        right = tuple(accumulate(reversed(temp[2:]),merge))
        for u,l,r in zip(children[v],left,reversed(right)):
            dp_up[u] = finalize(merge(l,r))

    res = [None]*N
    for v,l in enumerate(children):
        res[v] = reduce(merge,
                    (dp_down[u] for u in children[v]),
                    identity)
        res[v] = finalize(merge(res[v], dp_up[v]))

    return res

# Solve function using the rerooting algorithm
def solve(T):
    def merge(x,y):
        return (x*y)%MOD
    def finalize(x):
        return x+1

    return [v-1 for v in rerooting(T,merge,1,finalize)]

# Read input and solve
n = read_int()
parent_list = read_ints()  # 1-indexed parents

# Create edges from parent list
edges = [(p-1, i+1) for i, p in enumerate(parent_list)]

# Create rooted tree and solve
T = RootedTree(n, edges, 0)
result = solve(T)

# Print result
print(*result)
