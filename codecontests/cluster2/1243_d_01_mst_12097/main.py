#!/usr/bin/env python3

from library import read_ints

n, m = read_ints()

# Create a graph with edges of weight 1
# We use 0-indexing here (original problem used 1-indexing)
graph = [set() for _ in range(n)]

for _ in range(m):
    a, b = read_ints()
    a, b = a - 1, b - 1  # Convert to 0-indexing
    graph[a].add(b)
    graph[b].add(a)

# Find connected components in the complement graph (edges with weight 0)
# We use BFS to explore each connected component
component_count = 0
unused_vertices = set(range(n))

while unused_vertices:
    # Start a new component
    component_count += 1
    
    # Start BFS from an unused vertex
    current = {unused_vertices.pop()}
    
    while current:
        vertex = current.pop()
        
        # Find all unused vertices that are not connected to the current vertex by a weight-1 edge
        # These are connected by weight-0 edges
        next_vertices = {j for j in unused_vertices if j not in graph[vertex]}
        
        # Remove these vertices from unused_vertices
        unused_vertices.difference_update(next_vertices)
        
        # Add them to the current BFS queue
        current.update(next_vertices)

# The result is the number of components - 1
print(component_count - 1)