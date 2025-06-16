#!/usr/bin/env python3

from library import read_ints, Graph
from collections import deque

def find_bridges(graph):
    """Find all bridges in the graph using Tarjan's algorithm"""
    n = graph.n
    visited = [False] * n
    disc = [0] * n
    low = [0] * n
    parent = [-1] * n
    bridges = []
    time = [0]  # Use list to make it mutable in nested function
    
    def bridge_dfs(u):
        visited[u] = True
        disc[u] = low[u] = time[0]
        time[0] += 1
        
        for v in graph.neighbors(u):
            if not visited[v]:
                parent[v] = u
                bridge_dfs(v)
                low[u] = min(low[u], low[v])
                
                # If low[v] > disc[u], then (u,v) is a bridge
                if low[v] > disc[u]:
                    bridges.append((u, v))
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])
    
    for i in range(n):
        if not visited[i]:
            bridge_dfs(i)
    
    return bridges

def build_bridge_tree(graph):
    """Build bridge tree by removing bridges and creating tree of components"""
    bridges = find_bridges(graph)
    bridge_set = set(bridges) | set((v, u) for u, v in bridges)
    
    # Find connected components after removing bridges
    visited = [False] * graph.n
    components = []
    
    def dfs_component(node, component):
        visited[node] = True
        component.append(node)
        for neighbor in graph.neighbors(node):
            if not visited[neighbor] and (node, neighbor) not in bridge_set:
                dfs_component(neighbor, component)
    
    # Build components
    for i in range(graph.n):
        if not visited[i]:
            component = []
            dfs_component(i, component)
            components.append(component)
    
    # Create mapping from node to component index
    node_to_comp = {}
    for comp_idx, component in enumerate(components):
        for node in component:
            node_to_comp[node] = comp_idx
    
    # Build tree of components
    tree = Graph(len(components), directed=False)
    for u, v in bridges:
        comp_u = node_to_comp[u]
        comp_v = node_to_comp[v]
        if comp_u != comp_v:
            tree.add_edge(comp_u, comp_v)
    
    return tree

def find_tree_diameter(tree):
    """Find diameter of tree using two BFS"""
    if tree.n <= 1:
        return 0
    
    # First BFS from node 0 to find one end of diameter
    visited = [False] * tree.n
    queue = deque([(0, 0)])  # (node, distance)
    visited[0] = True
    farthest_node = 0
    max_dist = 0
    
    while queue:
        node, dist = queue.popleft()
        if dist > max_dist:
            max_dist = dist
            farthest_node = node
        
        for neighbor in tree.neighbors(node):
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append((neighbor, dist + 1))
    
    # Second BFS from farthest_node to find actual diameter
    visited = [False] * tree.n
    queue = deque([(farthest_node, 0)])
    visited[farthest_node] = True
    diameter = 0
    
    while queue:
        node, dist = queue.popleft()
        diameter = max(diameter, dist)
        
        for neighbor in tree.neighbors(node):
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append((neighbor, dist + 1))
    
    return diameter

def solve():
    n, m = read_ints()
    
    # Build graph
    graph = Graph(n, directed=False)
    for _ in range(m):
        u, v = read_ints()
        graph.add_edge(u-1, v-1)  # Convert to 0-indexed
    
    # Build bridge tree and find its diameter
    bridge_tree = build_bridge_tree(graph)
    diameter = find_tree_diameter(bridge_tree)
    
    print(diameter)

solve()
