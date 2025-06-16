#!/usr/bin/env python3

from library import DSU, read_ints

nodes, edges = read_ints()

# Create DSU for all nodes
dsu = DSU(nodes)

# Union connected nodes
for _ in range(edges):
    a, b = read_ints()
    dsu.union(a - 1, b - 1)  # Convert to 0-indexed

# The answer is 2^(nodes - connected_components)
# Each component can be treated as a single "super node"
components = dsu.component_count()
print(2**(nodes - components))
