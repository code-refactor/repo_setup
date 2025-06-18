#!/usr/bin/env python3

import sys
from collections import deque, defaultdict
from array import array
from typing import List, Tuple, Set, Dict, Optional, Callable, Any, Union, Iterator


# Input/Output Utilities
def fast_input() -> str:
    return sys.stdin.buffer.readline().decode('utf-8').strip()

def read_int() -> int:
    return int(fast_input())

def read_ints() -> List[int]:
    return list(map(int, fast_input().split()))

def read_int_pairs() -> List[Tuple[int, int]]:
    return [tuple(map(int, fast_input().split())) for _ in range(read_int())]

def yes_no(condition: bool, yes_str: str = "YES", no_str: str = "NO") -> str:
    return yes_str if condition else no_str

def read_line() -> str:
    return fast_input().strip()

def read_grid(n: int) -> List[str]:
    return [fast_input() for _ in range(n)]

def read_test_cases(func) -> None:
    t = read_int()
    for _ in range(t):
        func()


# Graph representation and utilities
# Graph utilities
def create_adj_list(n: int, edges: List[Tuple[int, int]], one_indexed: bool = True, directed: bool = False, weighted: bool = False) -> List[List[Any]]:
    """Create adjacency list from a list of edges"""
    adj = [[] for _ in range(n + (1 if one_indexed else 0))]
    offset = 1 if one_indexed else 0
    
    for edge in edges:
        if weighted:
            u, v, w = edge
        else:
            u, v = edge
            w = 1
            
        if one_indexed:
            u -= offset
            v -= offset
            
        if weighted:
            adj[u].append((v, w))
            if not directed:
                adj[v].append((u, w))
        else:
            adj[u].append(v)
            if not directed:
                adj[v].append(u)
    
    return adj

def read_graph(one_indexed: bool = True, directed: bool = False, weighted: bool = False) -> Tuple[int, int, List[List[Any]]]:
    """Read a graph from stdin and return vertices count, edges count, and adjacency list"""
    n, m = read_ints()
    adj = [[] for _ in range(n + (1 if one_indexed else 0))]
    offset = 1 if one_indexed else 0
    
    for _ in range(m):
        if weighted:
            u, v, w = read_ints()
        else:
            u, v = read_ints()
            w = 1
            
        if one_indexed:
            u -= offset
            v -= offset
            
        if weighted:
            adj[u].append((v, w))
            if not directed:
                adj[v].append((u, w))
        else:
            adj[u].append(v)
            if not directed:
                adj[v].append(u)
    
    return n, m, adj

class Graph:
    def __init__(self, n: int = 0, directed: bool = False):
        self._adj = [[] for _ in range(n)]
        self._n = n
        self._directed = directed
        
    def add_vertex(self): self._adj.append([]); self._n += 1; return self._n - 1
    def add_edge(self, u: int, v: int):
        self._adj[u].append(v)
        if not self._directed: self._adj[v].append(u)
    def neighbors(self, u: int): return self._adj[u]
    def vertices(self): return range(self._n)
    @property
    def adj(self): return self._adj
        
    @classmethod
    def from_edges(cls, n: int, edges: List[Tuple[int, int]], directed: bool = False) -> 'Graph':
        graph = cls(n, directed)
        for u, v in edges: graph.add_edge(u, v)
        return graph
        
    @classmethod
    def read(cls, one_indexed: bool = True, directed: bool = False) -> Tuple['Graph', int]:
        n, m, adj = read_graph(one_indexed, directed)
        graph = cls(n, directed); graph._adj = adj
        return graph, m


# Graph Algorithms
def dfs(adj: List[List[int]], start: int, visited: List[bool] = None) -> List[int]:
    """Recursive DFS traversal starting from a given node"""
    if visited is None: visited = [False] * len(adj)
    result = []
    
    def _dfs(node: int) -> None:
        visited[node] = True; result.append(node)
        for neighbor in adj[node]:
            if not visited[neighbor]: _dfs(neighbor)
    
    _dfs(start)
    return result

def dfs_iterative(adj: List[List[int]], start: int, visited: List[bool] = None) -> List[int]:
    """Iterative DFS traversal starting from a given node"""
    if visited is None: visited = [False] * len(adj)
    result, stack = [], [start]
    
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True; result.append(node)
            for neighbor in reversed(adj[node]):
                if not visited[neighbor]: stack.append(neighbor)
    
    return result

def bfs(adj: List[List[int]], start: int, visited: List[bool] = None) -> List[int]:
    """BFS traversal starting from a given node"""
    if visited is None: visited = [False] * len(adj)
    result, queue = [], deque([start])
    visited[start] = True
    
    while queue:
        node = queue.popleft(); result.append(node)
        for neighbor in adj[node]:
            if not visited[neighbor]:
                visited[neighbor] = True; queue.append(neighbor)
    
    return result

def count_components(adj: List[List[int]]) -> int:
    """Count the number of connected components in a graph"""
    n, visited, count = len(adj), [False] * len(adj), 0
    for i in range(n):
        if not visited[i]: dfs_iterative(adj, i, visited); count += 1
    return count

def find_components(adj: List[List[int]]) -> List[List[int]]:
    """Find all connected components in a graph"""
    n, visited, components = len(adj), [False] * len(adj), []
    for i in range(n):
        if not visited[i]: components.append(dfs_iterative(adj, i, visited))
    return components

def has_cycle(adj: List[List[int]], start: int = 0, visited: List[bool] = None, parent: int = -1) -> bool:
    """Check if a graph has a cycle using DFS"""
    if visited is None: visited = [False] * len(adj)
    visited[start] = True
    
    for neighbor in adj[start]:
        if not visited[neighbor]:
            if has_cycle(adj, neighbor, visited, start): return True
        elif neighbor != parent: return True
    return False

def count_cycles(adj: List[List[int]]) -> int:
    """Count cycles in an undirected graph"""
    n, visited, parent, cycle_count = len(adj), [False] * len(adj), [-1] * len(adj), 0
    
    def dfs_cycles(node):
        nonlocal cycle_count
        visited[node] = True
        for neighbor in adj[node]:
            if not visited[neighbor]: parent[neighbor] = node; dfs_cycles(neighbor)
            elif neighbor != parent[node]: cycle_count += 1
    
    for i in range(n):
        if not visited[i]: dfs_cycles(i)
    return cycle_count // 2

def has_cycle_directed(adj: List[List[int]]) -> bool:
    """Check if a directed graph has a cycle using DFS"""
    n, visited = len(adj), [0] * len(adj)  # 0: not visited, 1: in progress, 2: finished
    
    def dfs(node):
        visited[node] = 1  # Mark as in progress
        for neighbor in adj[node]:
            if visited[neighbor] == 0:
                if dfs(neighbor): return True
            elif visited[neighbor] == 1: return True
        visited[node] = 2  # Mark as finished
        return False
    
    for i in range(n):
        if visited[i] == 0 and dfs(i): return True
    return False
    
def is_cyclic_component(adj: List[List[int]], start: int, visited: List[bool] = None) -> bool:
    """Check if a connected component is a simple cycle (each vertex has degree 2)"""
    if visited is None: visited = [False] * len(adj)
    queue, visited[start], is_cyclic = deque([start]), True, True
    
    while queue:
        node = queue.popleft()
        if len(adj[node]) != 2: is_cyclic = False
        for neighbor in adj[node]:
            if not visited[neighbor]: visited[neighbor] = True; queue.append(neighbor)
    return is_cyclic

def count_cyclic_components(adj: List[List[int]]) -> int:
    """Count the number of connected components that are simple cycles"""
    n, visited, count = len(adj), [False] * len(adj), 0
    for i in range(n):
        if not visited[i] and is_cyclic_component(adj, i, visited): count += 1
    return count

def find_bridges(adj: List[List[int]]) -> List[Tuple[int, int]]:
    """Find all bridges in an undirected graph"""
    n, visited, disc, low, parent, bridges, time = len(adj), [False] * len(adj), [-1] * len(adj), [-1] * len(adj), [-1] * len(adj), [], 0
    
    def dfs_bridges(u):
        nonlocal time
        visited[u], disc[u], low[u] = True, time, time
        time += 1
        
        for v in adj[u]:
            if not visited[v]:
                parent[v] = u
                dfs_bridges(v)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]: bridges.append((u, v))
            elif v != parent[u]: low[u] = min(low[u], disc[v])
    
    for i in range(n):
        if not visited[i]: dfs_bridges(i)
    return bridges

def build_bridge_tree(adj: List[List[int]], edge_index: List[List[int]]) -> List[List[int]]:
    """Build a bridge tree from a graph"""
    v_count = len(adj)
    edge_count = sum(len(lst) for lst in adj) // 2
    
    preorder, parent, order, low = [0], [0] + [-1] * (v_count - 1), [0] + [-1] * (v_count - 1), [0] * v_count
    stack, rem, pre_i = [0], [len(dests) - 1 for dests in adj], 1
    
    while stack:
        v = stack.pop()
        while rem[v] >= 0:
            dest = adj[v][rem[v]]
            rem[v] -= 1
            if order[dest] == -1:
                preorder.append(dest)
                order[dest] = low[dest] = pre_i
                parent[dest] = v
                pre_i += 1
                stack.extend((v, dest))
                break
    
    is_bridge = array('b', [0]) * edge_count
    for v in reversed(preorder):
        for dest, ei in zip(adj[v], edge_index[v]):
            if dest != parent[v] and low[v] > low[dest]: low[v] = low[dest]
            if dest != parent[v] and order[v] < low[dest]: is_bridge[ei] = 1
    
    bridge_tree = [[] for _ in range(v_count)]
    stack, visited = [0], array('b', [1] + [0] * (v_count - 1))
    
    while stack:
        v = stack.pop()
        dq = deque([v])
        while dq:
            u = dq.popleft()
            for dest, ei in zip(adj[u], edge_index[u]):
                if visited[dest]: continue
                visited[dest] = 1
                if is_bridge[ei]:
                    bridge_tree[v].append(dest)
                    bridge_tree[dest].append(v)
                    stack.append(dest)
                else: dq.append(dest)
    
    return bridge_tree

def find_diameter(adj: List[List[int]]) -> Tuple[int, int, int, List[int]]:
    """Find the diameter of a tree and return end nodes and path"""
    n = len(adj)
    
    # Find one end of the diameter using BFS
    dq, end1 = deque([(0, -1)]), 0
    while dq:
        node, parent = dq.popleft()
        end1 = node
        for neighbor in adj[node]:
            if neighbor != parent: dq.append((neighbor, node))
    
    # Find the other end and compute the diameter
    prev = [-1] * n
    prev[end1] = -2
    dq, end2, diameter = deque([(end1, 0)]), end1, 0
    
    while dq:
        node, dist = dq.popleft()
        if dist > diameter: diameter, end2 = dist, node
        for neighbor in adj[node]:
            if prev[neighbor] == -1:
                prev[neighbor] = node
                dq.append((neighbor, dist + 1))
    
    return end1, end2, diameter, prev


# Disjoint Set Union (DSU)
class DisjointSetUnion:
    def __init__(self, n: int):
        """Initialize DSU with n nodes"""
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
    
    def find(self, x: int) -> int:
        """Find the representative of the set containing x with path compression"""
        if x != self.parent[x]: self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x: int, y: int) -> bool:
        """Unite the sets containing x and y. Return True if they were in different sets."""
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y: return False
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x], self.size[root_y] = root_y, self.size[root_y] + self.size[root_x]
        else:
            self.parent[root_y], self.size[root_x] = root_x, self.size[root_x] + self.size[root_y]
            if self.rank[root_x] == self.rank[root_y]: self.rank[root_x] += 1
        return True
    
    def get_size(self, x: int) -> int: return self.size[self.find(x)]
    def is_same_set(self, x: int, y: int) -> bool: return self.find(x) == self.find(y)
    def get_sets_count(self) -> int: return sum(1 for i in range(len(self.parent)) if i == self.parent[i])
    def get_all_roots(self) -> Set[int]: return {self.find(i) for i in range(len(self.parent))}
    
    def get_sets(self) -> Dict[int, List[int]]:
        """Get all sets as a dictionary mapping representatives to sets"""
        sets = defaultdict(list)
        for i in range(len(self.parent)): sets[self.find(i)].append(i)
        return dict(sets)