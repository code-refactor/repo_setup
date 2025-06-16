#!/usr/bin/env python3

from library import DSU, read_ints, print_yes_no
from collections import defaultdict

n, m = read_ints()

# Create DSU for all people
dsu = DSU(n + 1)  # 1-indexed
edge_count = defaultdict(int)

# Process friendships
for _ in range(m):
    p1, p2 = read_ints()
    dsu.union(p1, p2)
    
    # Count edges in each component
    root1 = dsu.find(p1)
    edge_count[root1] += 1

# Check if each component forms a complete graph
# A complete graph with k nodes has k*(k-1)/2 edges
valid = True
for root in edge_count:
    component_size = dsu.component_size(root)
    expected_edges = component_size * (component_size - 1) // 2
    if edge_count[root] != expected_edges:
        valid = False
        break

print_yes_no(valid)