#!/usr/bin/env python3

from library import parse_ints, parse_tree_edges, create_adjacency_list, count_degrees, find_leaves

n, s = parse_ints()

if n == 2:
    # Special case for a tree with 2 nodes (just one edge)
    parse_tree_edges(n)  # Just read the input, don't need to use it
    print(f"{s:.10f}")
    exit()
    
# Read the tree edges
edges = parse_tree_edges(n)
    
# Create adjacency list
adj_list = create_adjacency_list(n, edges)

# Count leaves (nodes with degree 1)
leaves = find_leaves(adj_list)
num_leaves = len(leaves)

# The minimum diameter is achieved by distributing the weight s evenly
# among all paths between leaves, which means 2*s/number_of_leaves
result = 2 * (s / num_leaves)
print(f"{result:.10f}")