#!/usr/bin/env python3

from library import read_ints
from collections import deque

def solve_test_case():
    # Read input for this test case
    n, m, a, b = read_ints()
    a -= 1  # Convert to 0-indexing
    b -= 1  # Convert to 0-indexing
    
    # Build the graph
    graph = [[] for _ in range(n)]
    for _ in range(m):
        u, v = read_ints()
        u -= 1  # Convert to 0-indexing
        v -= 1  # Convert to 0-indexing
        graph[u].append(v)
        graph[v].append(u)
    
    # Find connected components after removing a and b
    removed = [False] * n
    removed[a] = True
    removed[b] = True
    
    components = []
    visited = [False] * n
    
    for i in range(n):
        if not removed[i] and not visited[i]:
            component = []
            queue = deque([i])
            visited[i] = True
            
            while queue:
                node = queue.popleft()
                component.append(node)
                
                for neighbor in graph[node]:
                    if not removed[neighbor] and not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
            
            components.append(component)
    
    # For each component, check if it's connected to a and b
    a_only = 0
    b_only = 0
    
    for component in components:
        connected_to_a = False
        connected_to_b = False
        
        for node in component:
            for neighbor in graph[node]:
                if neighbor == a:
                    connected_to_a = True
                if neighbor == b:
                    connected_to_b = True
        
        # If component is only connected to a (and not b), add to a_only
        if connected_to_a and not connected_to_b:
            a_only += len(component)
        
        # If component is only connected to b (and not a), add to b_only
        if connected_to_b and not connected_to_a:
            b_only += len(component)
    
    # The answer is the product of these two values
    return a_only * b_only

# Read number of test cases
t = read_ints()[0]
results = []

for _ in range(t):
    results.append(str(solve_test_case()))

print('\n'.join(results))