#!/usr/bin/env python3

from library import read_ints, yes_no
from collections import defaultdict

def main():
    n, m = read_ints()
    
    # Build adjacency list
    adj = [[] for _ in range(n+1)]
    for _ in range(m):
        a, b = read_ints()
        adj[a].append(b)
        adj[b].append(a)
    
    # Check if each connected component is a complete graph
    visited = [False] * (n+1)
    
    for i in range(1, n+1):
        if not visited[i]:
            # Find all vertices in this component
            component = []
            stack = [i]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    component.append(node)
                    for neighbor in adj[node]:
                        if not visited[neighbor]:
                            stack.append(neighbor)
            
            # Count edges in this component
            edge_count = sum(len(adj[v]) for v in component) // 2
            
            # Check if it's a complete graph
            vertex_count = len(component)
            if edge_count != (vertex_count * (vertex_count - 1)) // 2:
                print("No")
                return
    
    print("Yes")

if __name__ == "__main__":
    main()
