#!/usr/bin/env python3

from library import parse_ints
from collections import defaultdict

# Read input
n, m = parse_ints()
colors = parse_ints()

# Create a graph of color adjacencies
color_graph = defaultdict(set)

# Process each edge
for _ in range(m):
    a, b = parse_ints()
    a -= 1  # Convert to 0-indexed
    b -= 1
    
    # Only add an edge if the colors are different
    if colors[a] != colors[b]:
        color_graph[colors[a]].add(colors[b])
        color_graph[colors[b]].add(colors[a])

# Find the color with the most diverse neighbors
max_diversity = 0
best_color = min(colors)  # Default to the minimum color

for color in sorted(color_graph.keys()):
    diversity = len(color_graph[color])
    
    if diversity > max_diversity:
        max_diversity = diversity
        best_color = color
    elif diversity == max_diversity:
        best_color = min(best_color, color)

print(best_color)