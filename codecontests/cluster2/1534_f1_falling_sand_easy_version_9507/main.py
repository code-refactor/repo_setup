#!/usr/bin/env python3

from library import read_ints, Graph

def strongly_connected_components(graph):
    """Tarjan's algorithm for finding strongly connected components"""
    n = graph.n
    index_counter = [0]
    stack = []
    lowlinks = [0] * n
    index = [0] * n
    on_stack = [False] * n
    index_initialized = [False] * n
    components = []
    
    def strongconnect(node):
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        index_initialized[node] = True
        stack.append(node)
        on_stack[node] = True
        
        for neighbor in graph.neighbors(node):
            if not index_initialized[neighbor]:
                strongconnect(neighbor)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbor])
            elif on_stack[neighbor]:
                lowlinks[node] = min(lowlinks[node], index[neighbor])
        
        if lowlinks[node] == index[node]:
            component = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                component.append(w)
                if w == node:
                    break
            components.append(component)
    
    for node in range(n):
        if not index_initialized[node]:
            strongconnect(node)
    
    return components

def solve():
    N, M = read_ints()
    
    # Read grid
    grid = []
    for _ in range(N):
        row = input().strip()
        grid.append([1 if c == "#" else 0 for c in row])
    
    # Sum of sand blocks
    sand_counts = read_ints()
    total_sand = sum(sand_counts)
    
    # Map sand positions to node indices
    sand_positions = []
    position_map = [[-1] * M for _ in range(N)]
    
    # Process columns from bottom to top
    for j in range(M):
        for i in range(N-1, -1, -1):
            if grid[i][j]:
                position_map[i][j] = len(sand_positions)
                sand_positions.append((i, j))
            elif i < N - 1:
                position_map[i][j] = position_map[i+1][j]
    
    # Build directed graph of sand movements
    graph = Graph(total_sand, directed=True)
    
    for k in range(total_sand):
        i, j = sand_positions[k]
        
        # Sand falls down
        if i < N - 1 and position_map[i+1][j] >= 0:
            graph.add_edge(k, position_map[i+1][j])
        
        # Sand can move up if there's a block
        if i > 0 and grid[i-1][j]:
            graph.add_edge(k, position_map[i-1][j])
        
        # Sand can move left
        if j > 0 and position_map[i][j-1] >= 0:
            graph.add_edge(k, position_map[i][j-1])
        
        # Sand can move right
        if j < M - 1 and position_map[i][j+1] >= 0:
            graph.add_edge(k, position_map[i][j+1])
    
    # Find strongly connected components
    components = strongly_connected_components(graph)
    
    # Count components that are sinks (no outgoing edges to other components)
    component_map = {}
    for comp_idx, component in enumerate(components):
        for node in component:
            component_map[node] = comp_idx
    
    sink_components = [True] * len(components)
    
    for node in range(total_sand):
        node_comp = component_map[node]
        for neighbor in graph.neighbors(node):
            neighbor_comp = component_map[neighbor]
            if node_comp != neighbor_comp:
                sink_components[node_comp] = False
    
    print(sum(sink_components))

solve()