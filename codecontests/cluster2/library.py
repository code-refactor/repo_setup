"""
Library file for cluster2.
This contains shared code that can be imported by problems in this cluster.
"""

from collections import defaultdict, deque
import sys


class DSU:
    """Disjoint Set Union (Union-Find) with path compression and union by rank"""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.components = n
    
    def find(self, x):
        """Find with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union by rank"""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        
        self.parent[py] = px
        self.size[px] += self.size[py]
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True
    
    def same_set(self, x, y):
        """Check if x and y are in same set"""
        return self.find(x) == self.find(y)
    
    def component_size(self, x):
        """Get size of component containing x"""
        return self.size[self.find(x)]
    
    def component_count(self):
        """Get total number of components"""
        return self.components


class Graph:
    """Graph representation with common operations"""
    
    def __init__(self, n, directed=False):
        self.n = n
        self.directed = directed
        self.adj = [[] for _ in range(n)]
        self.edge_count = 0
    
    def add_edge(self, u, v):
        """Add edge between u and v"""
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)
        self.edge_count += 1
    
    def neighbors(self, u):
        """Get neighbors of vertex u"""
        return self.adj[u]
    
    def vertices(self):
        """Get all vertices"""
        return range(self.n)
    
    def dfs(self, start, visited=None):
        """DFS traversal returning visited set"""
        if visited is None:
            visited = set()
        
        stack = [start]
        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                for neighbor in self.adj[v]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        return visited
    
    def dfs_recursive(self, start, visited=None):
        """Recursive DFS"""
        if visited is None:
            visited = set()
        
        visited.add(start)
        for neighbor in self.adj[start]:
            if neighbor not in visited:
                self.dfs_recursive(neighbor, visited)
        return visited
    
    def connected_components(self):
        """Find all connected components"""
        visited = set()
        components = []
        
        for v in range(self.n):
            if v not in visited:
                component = self.dfs(v, set())
                components.append(component)
                visited.update(component)
        
        return components
    
    def count_components(self):
        """Count number of connected components"""
        return len(self.connected_components())
    
    def has_cycle(self):
        """Detect cycle in undirected graph"""
        if self.directed:
            return self._has_cycle_directed()
        else:
            return self._has_cycle_undirected()
    
    def _has_cycle_undirected(self):
        """Detect cycle in undirected graph using DFS"""
        visited = set()
        
        def dfs_cycle(v, parent):
            visited.add(v)
            for neighbor in self.adj[v]:
                if neighbor not in visited:
                    if dfs_cycle(neighbor, v):
                        return True
                elif neighbor != parent:
                    return True
            return False
        
        for v in range(self.n):
            if v not in visited:
                if dfs_cycle(v, -1):
                    return True
        return False
    
    def _has_cycle_directed(self):
        """Detect cycle in directed graph using DFS"""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * self.n
        
        def dfs_cycle(v):
            color[v] = GRAY
            for neighbor in self.adj[v]:
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE and dfs_cycle(neighbor):
                    return True
            color[v] = BLACK
            return False
        
        for v in range(self.n):
            if color[v] == WHITE:
                if dfs_cycle(v):
                    return True
        return False


# Input/Output utilities
def read_int():
    """Read single integer"""
    return int(input())

def read_ints():
    """Read list of integers from a line"""
    return list(map(int, input().split()))

def read_graph(n, m, directed=False, one_indexed=True):
    """Read graph from standard input format"""
    graph = Graph(n, directed)
    for _ in range(m):
        u, v = read_ints()
        if one_indexed:
            u -= 1
            v -= 1
        graph.add_edge(u, v)
    return graph

def read_edges(m, one_indexed=True):
    """Read m edges and return as list of tuples"""
    edges = []
    for _ in range(m):
        u, v = read_ints()
        if one_indexed:
            u -= 1
            v -= 1
        edges.append((u, v))
    return edges

def print_yes_no(condition):
    """Print YES/NO based on condition"""
    print("YES" if condition else "NO")

def print_yes_no_custom(condition, yes_text="YES", no_text="NO"):
    """Print custom yes/no text based on condition"""
    print(yes_text if condition else no_text)


# Algorithm utilities
def count_connected_components(adj_list):
    """Count connected components given adjacency list"""
    n = len(adj_list)
    visited = [False] * n
    count = 0
    
    def dfs(v):
        visited[v] = True
        for neighbor in adj_list[v]:
            if not visited[neighbor]:
                dfs(neighbor)
    
    for v in range(n):
        if not visited[v]:
            dfs(v)
            count += 1
    
    return count

def detect_cycle_undirected(adj_list):
    """Detect cycle in undirected graph given adjacency list"""
    n = len(adj_list)
    visited = [False] * n
    
    def dfs(v, parent):
        visited[v] = True
        for neighbor in adj_list[v]:
            if not visited[neighbor]:
                if dfs(neighbor, v):
                    return True
            elif neighbor != parent:
                return True
        return False
    
    for v in range(n):
        if not visited[v]:
            if dfs(v, -1):
                return True
    return False

def build_adjacency_list(n, edges, directed=False):
    """Build adjacency list from list of edges"""
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        if not directed:
            adj[v].append(u)
    return adj