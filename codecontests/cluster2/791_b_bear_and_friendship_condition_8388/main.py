#!/usr/bin/env python3

from library import DSU, read_ints, print_yes_no_custom
from collections import defaultdict

n, m = read_ints()

# Create DSU for all people
dsu = DSU(n + 1)  # 1-indexed
edges_per_component = defaultdict(int)
edges = []

# Process friendships
for _ in range(m):
    a, b = read_ints()
    edges.append((a, b))
    dsu.union(a, b)

# Count edges in each component
for a, b in edges:
    # After union-find, both nodes should have same root
    root = dsu.find(a)
    edges_per_component[root] += 1

# Check if each component forms a complete graph
# A complete graph with k nodes has exactly k*(k-1)/2 edges
valid = True
for component_root in edges_per_component:
    component_size = dsu.component_size(component_root)
    expected_edges = component_size * (component_size - 1) // 2
    if edges_per_component[component_root] != expected_edges:
        valid = False
        break

print_yes_no_custom(valid, "Yes", "No")
