#!/usr/bin/env python3

from library import parse_ints
from sys import exit

# Read input
n, k = parse_ints()
distances = parse_ints()

# Group nodes by their distance from the chosen vertex
nodes_by_distance = [[] for _ in range(n+1)]
for node, dist in enumerate(distances):
    nodes_by_distance[dist].append(node)

# Check if the graph can be constructed:
# 1. There should be exactly one node with distance 0 (the chosen vertex)
# 2. The number of nodes at distance 1 shouldn't exceed k
if len(nodes_by_distance[0]) != 1 or len(nodes_by_distance[1]) > k:
    print(-1)
else:
    # Check if we can connect all nodes at distance i+1 to nodes at distance i
    # Each node at distance i can connect to at most k-1 nodes at distance i+1
    # (except for the source node which can connect to k nodes)
    for i in range(1, n):
        # If nodes at distance i can't connect to all nodes at distance i+1
        if len(nodes_by_distance[i]) * (k-1) < len(nodes_by_distance[i+1]):
            print(-1)
            exit(0)
    
    # Construct the graph
    edges = []
    
    for i in range(n):
        next_node_index = 0
        
        # Connect nodes at distance i to nodes at distance i+1
        if len(nodes_by_distance[i+1]) > 0:
            for j, node in enumerate(nodes_by_distance[i]):
                current_connections = 0
                
                # The root node (distance 0) can have k connections
                # Other nodes can have k-1 additional connections
                max_connections = k if i == 0 else k-1
                
                # Connect the current node to nodes at the next level
                while current_connections < max_connections and next_node_index < len(nodes_by_distance[i+1]):
                    # Add edge (1-indexed)
                    edges.append((node+1, nodes_by_distance[i+1][next_node_index]+1))
                    next_node_index += 1
                    current_connections += 1
    
    # Print the result
    print(len(edges))
    for edge in edges:
        print(f"{edge[0]} {edge[1]}")
