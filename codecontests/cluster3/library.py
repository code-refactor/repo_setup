"""
Library file for cluster3.
This contains shared code that can be imported by problems in this cluster.
"""

import sys
from types import GeneratorType

class TreeBuilder:
    @staticmethod
    def from_edges(n, edges, indexed=1, weighted=False):
        """Build adjacency list from edge list"""
        adj = [[] for _ in range(n)]
        for edge in edges:
            if weighted:
                u, v, w = edge
                u -= indexed
                v -= indexed
                adj[u].append((v, w))
                adj[v].append((u, w))
            else:
                u, v = edge
                u -= indexed
                v -= indexed
                adj[u].append(v)
                adj[v].append(u)
        return adj

class Utils:
    @staticmethod
    def fast_io():
        """Setup fast I/O"""
        import sys
        input = lambda: sys.stdin.readline().strip()
        return input
    
    @staticmethod
    def bootstrap(f, stack=[]):
        """Bootstrap decorator for deep recursion"""
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
    
    @staticmethod
    def set_recursion_limit(limit=200000):
        """Set recursion limit"""
        sys.setrecursionlimit(limit)
    
    @staticmethod
    def read_tree_edges(n, indexed=1, weighted=False):
        """Read tree edges from input"""
        edges = []
        for _ in range(n-1):
            if weighted:
                u, v, w = map(int, input().split())
                edges.append((u, v, w))
            else:
                u, v = map(int, input().split())
                edges.append((u, v))
        return edges
