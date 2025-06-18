#!/usr/bin/env python3

from library import read_ints

def main():
    n, m, k = read_ints()
    
    # Store edges that cannot be added to the tree
    forbidden_edges = set()
    
    # Count forbidden edges connected to vertex 1
    forbidden_from_root = 0
    
    for _ in range(m):
        a, b = read_ints()
        # Add forbidden edge
        forbidden_edges.add((min(a, b), max(a, b)))
        
        # Count forbidden edges connected to vertex 1
        if a == 1 or b == 1:
            forbidden_from_root += 1
    
    # Maximum possible degree for vertex 1
    max_degree_possible = n - 1 - forbidden_from_root
    
    # If max degree is less than k, it's impossible
    if max_degree_possible < k:
        print("impossible")
        return
    
    # Vertices that can potentially connect to vertex 1
    remaining = set(range(2, n+1))
    
    # Function to check if two vertices can be connected
    def can_connect(a, b):
        return (min(a, b), max(a, b)) not in forbidden_edges
    
    # DFS to find connected components through allowed edges
    def dfs(start):
        stack = [start]
        connected = set()
        
        while stack:
            node = stack.pop()
            connected.add(node)
            
            for next_node in list(remaining):
                if next_node not in connected and can_connect(node, next_node):
                    stack.append(next_node)
                    remaining.remove(next_node)
                    connected.add(next_node)
        
        return connected
    
    # Count possible connected components from vertex 1
    components = 0
    
    while remaining:
        # Find the next vertex that can connect to vertex 1
        can_start = False
        for vertex in list(remaining):
            if can_connect(1, vertex):
                remaining.remove(vertex)
                dfs(vertex)
                components += 1
                can_start = True
                break
        
        # If no vertex can connect to vertex 1, it's impossible
        if not can_start:
            print("impossible")
            return
    
    # Check if the number of components exceeds k
    if components > k:
        print("impossible")
    else:
        print("possible")

if __name__ == "__main__":
    main()