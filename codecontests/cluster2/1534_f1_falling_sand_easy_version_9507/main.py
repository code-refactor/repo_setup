#!/usr/bin/env python3

from library import read_ints
import sys

def scc(graph):
    """Find SCCs and count those without incoming edges from other SCCs"""
    n = len(graph)
    
    # Create reversed graph
    rev_graph = [[] for _ in range(n)]
    for i, neighbors in enumerate(graph):
        for v in neighbors:
            rev_graph[v].append(i)
    
    # First pass - topological sort
    done = [0] * n  # 0: not visited, 1: in progress, 2: finished
    finish_order = []
    
    for start in range(n):
        if done[start]:
            continue
        
        stack = []
        stack.append(~start)  # Mark with ~ for "post-visit" action
        stack.append(start)   # Regular visit
        
        while stack:
            node = stack.pop()
            
            if node < 0:  # Post-visit action (node is bitwise negated)
                node = ~node
                if done[node] == 2:
                    continue
                done[node] = 2
                finish_order.append(node)
                continue
            
            if done[node]:
                continue
            done[node] = 1
            
            stack.append(~node)  # Add post-visit action
            
            for neighbor in graph[node]:
                if done[neighbor]:
                    continue
                stack.append(neighbor)
    
    # Second pass - find SCCs
    done = [0] * n
    scc_ids = [0] * n
    scc_count = 0
    
    for start in reversed(finish_order):
        if done[start]:
            continue
        
        # Start a new SCC
        component = []
        stack = []
        stack.append(~start)
        stack.append(start)
        
        while stack:
            node = stack.pop()
            
            if node < 0:  # Post-visit
                node = ~node
                if done[node] == 2:
                    continue
                done[node] = 2
                component.append(node)
                scc_ids[node] = scc_count
                continue
            
            if done[node]:
                continue
            done[node] = 1
            
            stack.append(~node)
            
            for neighbor in rev_graph[node]:
                if done[neighbor]:
                    continue
                stack.append(neighbor)
        
        scc_count += 1
    
    # Find entry SCCs (no incoming edges from other SCCs)
    entry_sccs = [1] * scc_count
    
    for i, neighbors in enumerate(graph):
        for j in neighbors:
            if scc_ids[i] != scc_ids[j]:
                entry_sccs[scc_ids[j]] = 0
    
    return sum(entry_sccs)

def main():
    # Read input
    n, m = read_ints()
    grid = []
    for _ in range(n):
        grid.append([1 if c == '#' else 0 for c in input()])
    
    sand_counts = read_ints()
    total_sand = sum(sand_counts)
    
    # Map sand blocks to node indices
    node_indices = []
    node_grid = [[-1] * m for _ in range(n)]
    
    for j in range(m):
        for i in range(n-1, -1, -1):
            if grid[i][j]:
                node_indices.append((i << 20) | j)  # Encode position
                node_grid[i][j] = len(node_indices) - 1
            elif i < n-1:
                node_grid[i][j] = node_grid[i+1][j]
    
    # Build the graph
    graph = [[] for _ in range(total_sand)]
    mask = (1 << 20) - 1
    
    for k in range(total_sand):
        pos = node_indices[k]
        i, j = pos >> 20, pos & mask
        
        # Connect to adjacent blocks
        # Below
        if i < n-1 and node_grid[i+1][j] >= 0:
            graph[k].append(node_grid[i+1][j])
        # Above
        if i > 0 and grid[i-1][j]:
            graph[k].append(node_grid[i-1][j])
        # Left
        if j > 0 and node_grid[i][j-1] >= 0:
            graph[k].append(node_grid[i][j-1])
        # Right
        if j < m-1 and node_grid[i][j+1] >= 0:
            graph[k].append(node_grid[i][j+1])
    
    # Find SCCs and count entry points
    result = scc(graph)
    print(result)

# Fast input
input = lambda: sys.stdin.readline().rstrip()

# Run main
if __name__ == "__main__":
    main()