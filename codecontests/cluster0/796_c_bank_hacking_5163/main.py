#!/usr/bin/env python3

from library import parse_int, parse_ints, create_adjacency_list
from collections import Counter
import sys

# Read input
n = parse_int()
strengths = parse_ints()

# Add a sentinel value for easy computation of second maximum
strengths_with_sentinel = strengths + [-int(1e9+3)]

# Find the top two maximum strengths
c = Counter(strengths_with_sentinel)
top, sec = sorted(set(strengths_with_sentinel))[-1:-3:-1]

# Count occurrences of top and second max strengths in the neighborhood of each bank
top_cnt = [int(i == top) for i in strengths_with_sentinel]
sec_cnt = [int(i == sec) for i in strengths_with_sentinel]

# Read edges
edges = []
for _ in range(n-1):
    u, v = parse_ints()
    edges.append((u, v))
    
    # Count neighboring banks with top and second max strength
    if strengths[u-1] == top: top_cnt[v-1] += 1
    if strengths[v-1] == top: top_cnt[u-1] += 1
    if strengths[u-1] == sec: sec_cnt[v-1] += 1
    if strengths[v-1] == sec: sec_cnt[u-1] += 1

# Calculate minimum required computer strength
result = top + 2  # Initialize with a safe value

for i in range(n):
    # Skip banks that can't see all top-strength banks
    if top_cnt[i] < c[top]:
        continue
        
    # Calculate required strength based on top banks
    if top_cnt[i] == 1 and strengths[i] == top:
        current = top  # If this is the only top-strength bank
    else:
        current = top + 1  # Need to handle neighboring top-strength banks
        
    # Check second-max strength banks
    if sec_cnt[i] < c[sec]:
        current = max(current, sec + 2)  # Need to handle semi-neighboring second-max banks
        
    result = min(result, current)
    
print(result)
