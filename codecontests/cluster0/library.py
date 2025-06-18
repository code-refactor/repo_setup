#!/usr/bin/env python3

from collections import defaultdict, deque
import sys
import heapq
import re

# Input parsing helpers
def parse_int():
    """Parse a single integer from input."""
    return int(input())

def parse_ints(separator=' '):
    """Parse multiple integers from a single line."""
    return list(map(int, input().split(separator)))

def M():
    """Short form of map(int, input().split())."""
    return map(int, input().split())

def parse_graph_edges(m, one_indexed=True, weighted=False):
    """Parse m edges for a graph.
    
    Args:
        m: Number of edges to parse
        one_indexed: Whether the node indices are 1-indexed (default: True)
        weighted: Whether to parse edge weights (default: False)
        
    Returns:
        List of edge tuples: (u, v) or (u, v, w) if weighted
    """
    edges = []
    for _ in range(m):
        if weighted:
            u, v, w = parse_ints()
            if one_indexed:
                u -= 1
                v -= 1
            edges.append((u, v, w))
        else:
            u, v = parse_ints()
            if one_indexed:
                u -= 1
                v -= 1
            edges.append((u, v))
    return edges

def parse_tree_edges(n, one_indexed=True, weighted=False):
    """Parse n-1 edges for a tree with n nodes.
    
    Args:
        n: Number of nodes in the tree
        one_indexed: Whether the node indices are 1-indexed (default: True)
        weighted: Whether to parse edge weights (default: False)
        
    Returns:
        List of edge tuples: (u, v) or (u, v, w) if weighted
    """
    return parse_graph_edges(n-1, one_indexed, weighted)

# Graph/Tree representation
def create_adjacency_list(n, edges=None, directed=False, weighted=False):
    """Create an adjacency list for a graph.
    
    Args:
        n: Number of nodes
        edges: List of edge tuples (optional)
        directed: Whether the graph is directed (default: False)
        weighted: Whether the graph is weighted (default: False)
        
    Returns:
        Adjacency list as a list of lists
    """
    adj_list = [[] for _ in range(n)]
    
    if edges:
        if weighted:
            for u, v, w in edges:
                adj_list[u].append((v, w))
                if not directed:
                    adj_list[v].append((u, w))
        else:
            for u, v in edges:
                adj_list[u].append(v)
                if not directed:
                    adj_list[v].append(u)
                
    return adj_list

def add_edge(adj_list, u, v, directed=False, weight=None):
    """Add an edge to an adjacency list.
    
    Args:
        adj_list: Adjacency list
        u, v: Nodes to connect
        directed: Whether the edge is directed (default: False)
        weight: Edge weight (optional)
    """
    if weight is not None:
        adj_list[u].append((v, weight))
        if not directed:
            adj_list[v].append((u, weight))
    else:
        adj_list[u].append(v)
        if not directed:
            adj_list[v].append(u)

# Graph/Tree traversal
def bfs(adj_list, start):
    """Breadth-first search traversal.
    
    Args:
        adj_list: Adjacency list
        start: Starting node
        
    Returns:
        Dictionary of visited nodes with their distance from start
    """
    n = len(adj_list)
    visited = [False] * n
    distances = [-1] * n
    queue = deque([start])
    
    visited[start] = True
    distances[start] = 0
    
    while queue:
        node = queue.popleft()
        for neighbor in adj_list[node]:
            if not visited[neighbor]:
                visited[neighbor] = True
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)
                
    return distances

def dfs(adj_list, start):
    """Depth-first search traversal.
    
    Args:
        adj_list: Adjacency list
        start: Starting node
        
    Returns:
        List of visited nodes
    """
    n = len(adj_list)
    visited = [False] * n
    result = []
    
    def _dfs(node):
        visited[node] = True
        result.append(node)
        for neighbor in adj_list[node]:
            if not visited[neighbor]:
                _dfs(neighbor)
    
    _dfs(start)
    return result

def dfs_with_stack(adj_list, start):
    """DFS traversal using a stack instead of recursion.
    
    Args:
        adj_list: Adjacency list
        start: Starting node
        
    Returns:
        List of visited nodes
    """
    n = len(adj_list)
    visited = [False] * n
    result = []
    stack = [start]
    
    while stack:
        node = stack.pop()
        if not visited[node]:
            visited[node] = True
            result.append(node)
            for neighbor in reversed(adj_list[node]):
                if not visited[neighbor]:
                    stack.append(neighbor)
    
    return result

# Graph/Tree properties
def count_degrees(adj_list):
    """Count the degree of each node.
    
    Args:
        adj_list: Adjacency list
        
    Returns:
        List where index i contains the degree of node i
    """
    return [len(neighbors) for neighbors in adj_list]

def find_leaves(adj_list):
    """Find all leaf nodes in a tree.
    
    Args:
        adj_list: Adjacency list
        
    Returns:
        List of leaf nodes (nodes with degree 1)
    """
    return [i for i, neighbors in enumerate(adj_list) if len(neighbors) == 1]

def is_leaf(adj_list, node):
    """Check if a node is a leaf.
    
    Args:
        adj_list: Adjacency list
        node: Node to check
        
    Returns:
        True if the node is a leaf (degree 1), False otherwise
    """
    return len(adj_list[node]) == 1

def calculate_depths(adj_list, root):
    """Calculate the depth of each node from the root.
    
    Args:
        adj_list: Adjacency list
        root: Root node
        
    Returns:
        List where index i contains the depth of node i
    """
    return bfs(adj_list, root)

def calculate_subtree_sizes(adj_list, root):
    """Calculate the size of the subtree rooted at each node.
    
    Args:
        adj_list: Adjacency list
        root: Root node
        
    Returns:
        List where index i contains the size of the subtree rooted at node i
    """
    n = len(adj_list)
    sizes = [1] * n  # Initialize with 1 (count the node itself)
    
    order = tree_order(adj_list, root)
    
    for node in order:
        for neighbor in adj_list[node]:
            # Skip parent (already counted in the parent's size)
            # In a tree, we can detect the parent by checking if it's in the path to the root
            if neighbor not in order or order.index(neighbor) > order.index(node):
                sizes[node] += sizes[neighbor]
    
    return sizes

def is_bipartite_with_colors(adj_list):
    """Check if a graph is bipartite and return the coloring.
    
    Args:
        adj_list: Adjacency list
        
    Returns:
        Tuple of (is_bipartite, colors) where colors[i] is the color of node i
    """
    n = len(adj_list)
    colors = [-1] * n  # -1: not colored, 0: first color, 1: second color
    
    for start in range(n):
        if colors[start] == -1:
            colors[start] = 0
            queue = deque([start])
            
            while queue:
                node = queue.popleft()
                for neighbor in adj_list[node]:
                    if colors[neighbor] == -1:
                        colors[neighbor] = 1 - colors[node]
                        queue.append(neighbor)
                    elif colors[neighbor] == colors[node]:
                        return False, colors
    
    return True, colors

def find_diameter(adj_list):
    """Find the diameter of a tree.
    
    Args:
        adj_list: Adjacency list
        
    Returns:
        The diameter of the tree (longest path between any two nodes)
    """
    # Find the farthest node from any arbitrary node
    distances = bfs(adj_list, 0)
    farthest_node = distances.index(max(distances))
    
    # Find the farthest node from the previously found node
    distances = bfs(adj_list, farthest_node)
    diameter = max(distances)
    
    return diameter

def get_furthest_node(adj_list, start):
    """Find the furthest node from the start node.
    
    Args:
        adj_list: Adjacency list
        start: Starting node
        
    Returns:
        Tuple of (furthest_node, distance)
    """
    distances = bfs(adj_list, start)
    furthest = distances.index(max(distances))
    return furthest, distances[furthest]

def find_root(parent_array):
    """Find the root of a tree given a parent array.
    
    Args:
        parent_array: List where parent_array[i] is the parent of node i
        
    Returns:
        The root node
    """
    for i, parent in enumerate(parent_array):
        if parent == -1 or parent == 0:
            return i
    return -1  # No root found

# Common algorithms
def is_bipartite(adj_list):
    """Check if a graph is bipartite.
    
    Args:
        adj_list: Adjacency list
        
    Returns:
        True if the graph is bipartite, False otherwise
    """
    n = len(adj_list)
    colors = [-1] * n  # -1: not colored, 0: first color, 1: second color
    
    for start in range(n):
        if colors[start] == -1:
            colors[start] = 0
            queue = deque([start])
            
            while queue:
                node = queue.popleft()
                for neighbor in adj_list[node]:
                    if colors[neighbor] == -1:
                        colors[neighbor] = 1 - colors[node]
                        queue.append(neighbor)
                    elif colors[neighbor] == colors[node]:
                        return False
    
    return True

# Advanced traversal functions
def dfs_with_parent(adj_list, start, parent=-1):
    """DFS traversal that keeps track of parent nodes.
    
    Args:
        adj_list: Adjacency list
        start: Starting node
        parent: Parent of the starting node (default: -1)
        
    Returns:
        Visited nodes and their parents as a list of (node, parent) tuples
    """
    visited = set([start])
    result = [(start, parent)]
    
    for neighbor in adj_list[start]:
        if neighbor != parent:
            result.extend(dfs_with_parent(adj_list, neighbor, start))
    
    return result

def dfs_iterative(adj_list, start, parent=-1):
    """Iterative DFS traversal that avoids recursion stack issues.
    
    Args:
        adj_list: Adjacency list
        start: Starting node
        parent: Parent of the starting node (default: -1)
        
    Returns:
        List of visited nodes
    """
    n = len(adj_list)
    visited = [False] * n
    result = []
    stack = [(start, parent, 0)]  # (node, parent, neighbors_processed)
    
    while stack:
        node, parent, idx = stack[-1]
        
        if not visited[node]:
            visited[node] = True
            result.append(node)
            
        if idx < len(adj_list[node]):
            neighbor = adj_list[node][idx]
            stack[-1] = (node, parent, idx + 1)
            
            if neighbor != parent and not visited[neighbor]:
                stack.append((neighbor, node, 0))
        else:
            stack.pop()
    
    return result

def tree_order(adj_list, root):
    """Get the nodes in an order suitable for tree DP algorithms.
    
    Args:
        adj_list: Adjacency list
        root: Root node
        
    Returns:
        List of nodes in a bottom-up order (leaves to root)
    """
    n = len(adj_list)
    visited = [False] * n
    result = []
    stack = [(root, -1)]
    
    while stack:
        node, parent = stack[-1]
        
        # Check if all children have been processed
        all_children_processed = True
        for neighbor in adj_list[node]:
            if neighbor != parent and not visited[neighbor]:
                all_children_processed = False
                stack.append((neighbor, node))
                
        if all_children_processed:
            visited[node] = True
            result.append(node)
            stack.pop()
    
    return result

# String and pattern functions
def is_lucky(num):
    """Check if a number is lucky (contains only 4 and 7).
    
    Args:
        num: The number to check (as a string or int)
        
    Returns:
        True if the number is lucky, False otherwise
    """
    if isinstance(num, int):
        num = str(num)
    return re.fullmatch("[47]+", num) is not None

# Dijkstra's algorithm for shortest paths
def dijkstra(graph, start):
    """Find shortest paths from start node to all other nodes using Dijkstra's algorithm.
    
    Args:
        graph: Weighted adjacency list where graph[u] contains (weight, node) tuples
        start: Starting node
        
    Returns:
        Tuple of (distances, previous) where distances[i] is the shortest distance from start to i,
        and previous[i] is the previous node on the shortest path from start to i
    """
    n = len(graph)
    dist = [float('inf')] * n
    prev = [-1] * n
    dist[start] = 0
    
    pq = [(0, start)]  # (distance, node)
    
    while pq:
        d, node = heapq.heappop(pq)
        
        if d > dist[node]:
            continue
            
        for weight, neighbor in graph[node]:
            if dist[node] + weight < dist[neighbor]:
                dist[neighbor] = dist[node] + weight
                prev[neighbor] = node
                heapq.heappush(pq, (dist[neighbor], neighbor))
                
    return dist, prev

# Tree traversal functions
def postorder_traversal(adj_list, start, parent=-1):
    """Perform postorder traversal starting from a node.
    
    Args:
        adj_list: Adjacency list
        start: Starting node
        parent: Parent of the starting node (default: -1)
        
    Returns:
        List of nodes in postorder traversal
    """
    result = []
    
    for neighbor in adj_list[start]:
        if neighbor != parent:
            result.extend(postorder_traversal(adj_list, neighbor, start))
    
    result.append(start)
    return result

def topological_sort(adj_list):
    """Perform a topological sort on a directed acyclic graph.
    
    Args:
        adj_list: Adjacency list
        
    Returns:
        List of nodes in topological order
    """
    n = len(adj_list)
    visited = [False] * n
    result = []
    
    def dfs(node):
        visited[node] = True
        for neighbor in adj_list[node]:
            if not visited[neighbor]:
                dfs(neighbor)
        result.append(node)
    
    for i in range(n):
        if not visited[i]:
            dfs(i)
            
    return result[::-1]

# Utility functions
def fast_input():
    """Set up fast input reading."""
    return sys.stdin.readline