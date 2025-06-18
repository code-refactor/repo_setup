#!/usr/bin/env python3

from library import parse_ints
from collections import defaultdict
from bisect import bisect_left

# Read input
n, m = parse_ints()

# Initialize data structures
count = [0] * n  # Count of occurrences for each coder
coders_map = defaultdict()  # Map to track pairs of coders
answer = [0] * n  # Answer for each coder

# Read accusation pairs and build data structures
for _ in range(n):
    x, y = parse_ints()
    x, y = x - 1, y - 1  # Convert to 0-indexed
    
    # Ensure the pair is ordered for consistent keys
    key = (min(x, y), max(x, y))
    
    # Count the number of times this pair appears
    if key in coders_map:
        coders_map[key] += 1
    else:
        coders_map[key] = 1
        
    # Count each coder's occurrences
    count[x] += 1
    count[y] += 1

# Handle special case for each pair
for (x, y), val in coders_map.items():
    # This condition checks if selecting this pair would satisfy exactly the minimum requirement
    if count[x] + count[y] >= m and count[x] + count[y] - val < m:
        answer[x] -= 1
        answer[y] -= 1

# Sort the counts for binary search
sorted_counts = count.copy()
sorted_counts.sort()

# Calculate the number of valid pairs for each coder
for i in range(n):
    # Count how many coders can be paired with this one to satisfy the requirement
    answer[i] += n - bisect_left(sorted_counts, m - count[i])
    
    # Adjust for self-pairing case
    if 2 * count[i] >= m:
        answer[i] -= 1

# Each pair is counted twice, so divide by 2
print(sum(answer) // 2)
