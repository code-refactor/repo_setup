#!/usr/bin/env python3

from library import read_int, read_ints, Graph
from collections import deque

def solve():
    t = read_int()
    results = []
    
    for _ in range(t):
        n, m, a, b = read_ints()
        a -= 1  # Convert to 0-indexed
        b -= 1
        
        # Build graph
        graph = Graph(n, directed=False)
        for _ in range(m):
            u, v = read_ints()
            graph.add_edge(u-1, v-1)  # Convert to 0-indexed
        
        # Find connected components excluding vertices a and b
        visited = [False] * n
        visited[a] = True  # Mark as visited to exclude
        visited[b] = True
        
        components = []
        component_connects_to = []  # Which special vertices each component connects to
        
        for i in range(n):
            if not visited[i]:
                # BFS to find component
                component = []
                connects_to = set()
                
                queue = deque([i])
                visited[i] = True
                
                while queue:
                    node = queue.popleft()
                    component.append(node)
                    
                    for neighbor in graph.neighbors(node):
                        if neighbor == a:
                            connects_to.add("A")
                        elif neighbor == b:
                            connects_to.add("B")
                        elif not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
                
                components.append(component)
                component_connects_to.append(connects_to)
        
        # Count nodes in components that connect only to A or only to B
        A_only = 0
        B_only = 0
        
        for component, connects_to in zip(components, component_connects_to):
            if connects_to == {"A"}:
                A_only += len(component)
            elif connects_to == {"B"}:
                B_only += len(component)
        
        results.append(str(A_only * B_only))
    
    print("\n".join(results))

solve()
