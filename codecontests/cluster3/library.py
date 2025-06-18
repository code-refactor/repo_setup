#!/usr/bin/env python3

import os
import sys
from io import BytesIO, IOBase
from types import GeneratorType
from collections import defaultdict, deque
import heapq
import math
from functools import lru_cache

# Fast I/O utilities
BUFSIZE = 8192

class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


def setup_io():
    """Set up fast I/O for competitive programming"""
    sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
    return lambda: sys.stdin.readline().rstrip("\r\n")


# Utility functions for parsing input
def read_int():
    """Read a single integer from stdin"""
    return int(input())


def read_ints():
    """Read a list of integers from stdin"""
    return list(map(int, input().split()))


def read_int_tuple():
    """Read a tuple of integers from stdin"""
    return tuple(map(int, input().split()))


# Recursion utilities
def bootstrap(f, stack=[]):
    """Decorator to make a recursive function non-recursive to avoid stack overflow"""
    def wrappedfunc(*args, **kwargs):
        if stack:
            return f(*args, **kwargs)
        else:
            to = f(*args, **kwargs)
            while True:
                if type(to) is GeneratorType:
                    stack.append(to)
                    to = next(to)
                else:
                    stack.pop()
                    if not stack:
                        break
                    to = stack[-1].send(to)
            return to
    return wrappedfunc


# Graph and Tree utilities
def create_adjacency_list(n, edges, directed=False, one_indexed=True):
    """Create an adjacency list from a list of edges"""
    adj = [[] for _ in range(n + 1 if one_indexed else n)]
    
    for edge in edges:
        u, v = edge[:2]
        w = edge[2] if len(edge) > 2 else 1
        
        adj[u].append((v, w))
        if not directed:
            adj[v].append((u, w))
    
    return adj


def create_tree_from_input(n, one_indexed=True):
    """Create a tree from input. Returns adjacency list."""
    offset = 1 if one_indexed else 0
    adj = [[] for _ in range(n + offset)]
    
    for _ in range(n - 1):
        u, v = read_int_tuple()
        adj[u].append(v)
        adj[v].append(u)
    
    return adj


def create_weighted_tree_from_input(n, one_indexed=True):
    """Create a weighted tree from input. Returns adjacency list with weights."""
    offset = 1 if one_indexed else 0
    adj = [[] for _ in range(n + offset)]
    
    for _ in range(n - 1):
        u, v, w = read_int_tuple()
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    return adj


# Tree traversal algorithms
def dfs(graph, start, visited=None):
    """Iterative DFS implementation"""
    if visited is None:
        visited = set()
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.add(vertex)
            stack.extend(reversed([node for node in graph[vertex] if node not in visited]))
    return visited


def dfs_recursive(graph, node, visited=None):
    """Recursive DFS implementation"""
    if visited is None:
        visited = set()
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs_recursive(graph, neighbor, visited)
    return visited


def bfs(graph, start):
    """BFS implementation"""
    visited = set([start])
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return visited


# Tree computation algorithms
def compute_subtree_size(adj, root=1):
    """Compute the size of each subtree in a tree"""
    n = len(adj)
    size = [0] * n
    
    def dfs(node, parent):
        size[node] = 1
        for child in adj[node]:
            if child != parent:
                dfs(child, node)
                size[node] += size[child]
    
    dfs(root, -1)
    return size


def compute_tree_depth(adj, root=1):
    """Compute the depth of each node in a tree"""
    n = len(adj)
    depth = [0] * n
    
    def dfs(node, parent, d):
        depth[node] = d
        for child in adj[node]:
            if child != parent:
                dfs(child, node, d + 1)
    
    dfs(root, -1, 0)
    return depth


def tree_rerooting(adj, values):
    """Re-root a tree to find optimal root"""
    n = len(adj)
    subtree_sum = [0] * n
    ans = [0] * n
    
    def dfs1(node, parent):
        subtree_sum[node] = values[node]
        for child in adj[node]:
            if child != parent:
                dfs1(child, node)
                subtree_sum[node] += subtree_sum[child]
    
    def dfs2(node, parent):
        if parent != -1:
            ans[node] = ans[parent] + (subtree_sum[1] - subtree_sum[node]) - subtree_sum[node]
        else:
            ans[node] = subtree_sum[node]
        
        for child in adj[node]:
            if child != parent:
                dfs2(child, node)
    
    dfs1(1, -1)
    dfs2(1, -1)
    return ans


# Tree computation using bootstrap (to avoid recursion limit)
@bootstrap
def compute_subtree_size_bootstrap(adj, node, parent, size):
    """Compute subtree sizes using bootstrap to avoid stack overflow"""
    size[node] = 1
    for child, _ in adj[node]:
        if child != parent:
            yield compute_subtree_size_bootstrap(adj, child, node, size)
            size[node] += size[child]
    yield


@bootstrap
def compute_tree_depth_bootstrap(adj, node, parent, depth, current_depth=0):
    """Compute node depths using bootstrap to avoid stack overflow"""
    depth[node] = current_depth
    for child, _ in adj[node]:
        if child != parent:
            yield compute_tree_depth_bootstrap(adj, child, node, depth, current_depth + 1)
    yield


# Dynamic programming on trees
def tree_dp(adj, root=1, process_node=None, combine_results=None):
    """Generic tree DP framework"""
    n = len(adj)
    dp = [0] * n
    
    def dfs(node, parent):
        # Process children first
        child_results = []
        for child in adj[node]:
            if child != parent:
                child_result = dfs(child, node)
                child_results.append(child_result)
        
        # Combine results from children
        if combine_results:
            combined = combine_results(child_results)
        else:
            combined = sum(child_results) if child_results else 0
        
        # Process current node
        if process_node:
            dp[node] = process_node(node, combined)
        else:
            dp[node] = combined + 1  # Default: count nodes in subtree
        
        return dp[node]
    
    dfs(root, -1)
    return dp


# Union-Find (Disjoint Set Union)
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.count = n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x
            
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        
        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1
            
        self.count -= 1
        return True
    
    def get_size(self, x):
        return self.size[self.find(x)]
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)