#!/usr/bin/env python3

from library import parse_int, parse_ints
from collections import Counter, deque

def main():
    # Read input
    n = parse_int()
    
    # For n=1, there's only the root node
    if n == 1:
        print(1)
        return
        
    # Read parent nodes
    parents = parse_ints()
    
    # Create adjacency list for the tree (directed from child to parent)
    adj_list = [[] for _ in range(n+1)]
    
    # Build the directed tree from parent array
    for i in range(n-1):
        parent = parents[i]
        child = i + 2  # Since children start from index 2
        adj_list[parent].append(child)
    
    # Calculate node depths using BFS
    depths = [0] * (n+1)
    
    # BFS starting from the root (node 1)
    queue = deque([1])
    visited = [False] * (n+1)
    visited[1] = True
    
    while queue:
        node = queue.popleft()
        for child in adj_list[node]:
            if not visited[child]:
                visited[child] = True
                depths[child] = depths[node] + 1
                queue.append(child)
    
    # Count nodes at each depth
    depth_counts = Counter(depths[1:n+1])  # Skip index 0 which is unused
    
    # Count depths with odd number of nodes
    # Nodes with odd counts will have one apple that doesn't annihilate
    # Those apples will eventually reach the root
    odd_depths = sum(1 for count in depth_counts.values() if count % 2 == 1)
    
    print(odd_depths)

if __name__ == "__main__":
    main()
