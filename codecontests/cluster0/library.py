"""
Library file for cluster0.
This contains shared code that can be imported by problems in this cluster.
"""

import sys
import io
import os
from collections import defaultdict, deque, Counter
import heapq
import threading

# Input/Output Utilities
def fast_input():
    """Fast input reading using io.BytesIO"""
    return io.BytesIO(os.read(0, os.fstat(0).st_size)).readline

def ints():
    """Parse integers from input line"""
    return map(int, input().split())

def int_inp():
    """Single integer input"""
    return int(input())

# Graph Construction
def adj_list(n, edges=None, zero_indexed=True):
    """Build adjacency list from edges"""
    graph = [[] for _ in range(n)]
    if edges:
        for edge in edges:
            u, v = edge
            if not zero_indexed:
                u, v = u-1, v-1
            graph[u].append(v)
            graph[v].append(u)
    return graph

def weighted_adj_list(n, edges=None, zero_indexed=True):
    """Build weighted adjacency list from edges"""
    graph = [[] for _ in range(n)]
    if edges:
        for edge in edges:
            if len(edge) == 3:
                u, v, w = edge
            else:
                u, v = edge
                w = 1
            if not zero_indexed:
                u, v = u-1, v-1
            graph[u].append((w, v))
            graph[v].append((w, u))
    return graph

def tree_from_parents(parents, root=0):
    """Build tree from parent array"""
    n = len(parents)
    children = [[] for _ in range(n)]
    for i, p in enumerate(parents):
        if p != -1 and i != root:
            children[p].append(i)
    return children

def add_edge(graph, u, v, directed=False):
    """Add edge to graph"""
    graph[u].append(v)
    if not directed:
        graph[v].append(u)

# Tree/Graph Traversal
def dfs_iterative(graph, start, callback=None):
    """Iterative DFS with callback"""
    OBSERVE, CHECK = 0, 1
    stack = [(OBSERVE, start, -1)]
    result = []
    
    while stack:
        state, v, parent = stack.pop()
        if state == OBSERVE:
            stack.append((CHECK, v, parent))
            for u in graph[v]:
                if u != parent:
                    stack.append((OBSERVE, u, v))
        else:
            if callback:
                callback(v, parent)
            result.append(v)
    return result

def dfs_recursive(graph, start, visited=None, callback=None, parent=-1):
    """Recursive DFS with callback"""
    if visited is None:
        visited = [False] * len(graph)
    
    visited[start] = True
    if callback:
        callback(start, parent)
    
    for neighbor in graph[start]:
        if not visited[neighbor]:
            dfs_recursive(graph, neighbor, visited, callback, start)

def bfs(graph, start, callback=None):
    """BFS traversal with callback"""
    n = len(graph)
    visited = [False] * n
    queue = deque([start])
    visited[start] = True
    result = []
    
    while queue:
        v = queue.popleft()
        if callback:
            callback(v)
        result.append(v)
        
        for u in graph[v]:
            if not visited[u]:
                visited[u] = True
                queue.append(u)
    return result

def topo_order_tree(graph, root):
    """Topological ordering for trees (parent-child relationships)"""
    result = [(root, None)]
    i = 0
    while i < len(result):
        u, parent = result[i]
        i += 1
        for v in graph[u]:
            if v != parent:
                result.append((v, u))
    return result

# Tree Analysis
def subtree_sizes(graph, root):
    """Calculate subtree sizes using iterative DFS (matches original dfs function)"""
    n = len(graph)
    size = [0] * n
    
    def dfs(node, parent):
        for neighbor in graph[node]:
            if neighbor != parent:
                size[node] += dfs(neighbor, node)
        return size[node] + 1
    
    dfs(root, -1)
    return size

def find_leaves(graph, ignore_root=True):
    """Find all leaf nodes"""
    leaves = []
    for i in range(len(graph)):
        if len(graph[i]) == 1:
            if not ignore_root or i != 0:
                leaves.append(i)
    return leaves

def tree_diameter(graph):
    """Find tree diameter using 2-BFS approach"""
    n = len(graph)
    if n == 0:
        return 0, []
    
    # First BFS from node 0
    def bfs_farthest(start):
        dist = [-1] * n
        dist[start] = 0
        queue = deque([start])
        farthest = start
        
        while queue:
            v = queue.popleft()
            for u in graph[v]:
                if dist[u] == -1:
                    dist[u] = dist[v] + 1
                    queue.append(u)
                    if dist[u] > dist[farthest]:
                        farthest = u
        return farthest, dist[farthest]
    
    # Find one end of diameter
    end1, _ = bfs_farthest(0)
    # Find other end of diameter
    end2, diameter = bfs_farthest(end1)
    
    return diameter, (end1, end2)

def tree_depth_bfs(graph, root):
    """Calculate maximum depth from root using BFS (like original solution)"""
    depth = 1
    next_level = graph[root][:]
    
    while len(next_level) > 0:
        depth += 1
        children = next_level[:]
        next_level = []
        for child in children:
            next_level += graph[child]
    
    return depth

def tree_depth(graph, root):
    """Calculate maximum depth from root (number of levels)"""
    if not graph[root]:
        return 1
    
    max_depth = 1
    
    def dfs(v, parent, depth):
        nonlocal max_depth
        max_depth = max(max_depth, depth)
        for u in graph[v]:
            if u != parent:
                dfs(u, v, depth + 1)
    
    dfs(root, -1, 1)
    return max_depth

def tree_depths_all(graph, root):
    """Calculate depth of all nodes from root"""
    n = len(graph)
    depth = [-1] * n
    depth[root] = 0
    queue = deque([root])
    
    while queue:
        v = queue.popleft()
        for u in graph[v]:
            if depth[u] == -1:
                depth[u] = depth[v] + 1
                queue.append(u)
    return depth

# Shortest Paths
def dijkstra(graph, start):
    """Dijkstra's algorithm for shortest paths"""
    n = len(graph)
    INF = float('inf')
    dist = [INF] * n
    prev = [-1] * n
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        d, v = heapq.heappop(pq)
        if dist[v] < d:
            continue
        
        for w, u in graph[v]:
            if dist[u] > dist[v] + w:
                dist[u] = dist[v] + w
                prev[u] = v
                heapq.heappush(pq, (dist[u], u))
    
    return dist, prev

# Tree DP Framework
def tree_dp_up_down(graph, root, up_func, down_func):
    """Up-down DP pattern on trees"""
    n = len(graph)
    dp_up = [0] * n
    dp_down = [0] * n
    
    # Up pass (from leaves to root)
    order = topo_order_tree(graph, root)
    for u, parent in reversed(order):
        if parent is not None:
            dp_up[u] = up_func(u, parent, graph, dp_up)
    
    # Down pass (from root to leaves)
    for u, parent in order:
        if parent is not None:
            dp_down[u] = down_func(u, parent, graph, dp_up, dp_down)
    
    return dp_up, dp_down

# Utilities
def degree_count(edges, n):
    """Count degrees of all vertices"""
    degree = [0] * n
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    return degree

def counter_dict(arr):
    """Dictionary counter implementation"""
    count = {}
    for x in arr:
        count[x] = count.get(x, 0) + 1
    return count

# Threading setup for deep recursion
def setup_threading():
    """Setup threading for deep recursion problems"""
    sys.setrecursionlimit(300000)
    threading.stack_size(10 ** 8)

def run_with_threading(func):
    """Run function with threading"""
    setup_threading()
    t = threading.Thread(target=func)
    t.start()
    t.join()

# Common input patterns
M = lambda: map(int, input().split())