#!/usr/bin/env python3

from library import read_ints, yes_no

bound, m = read_ints()

# If there's only one pair, the answer is always YES
if m == 1:
    print("YES")
    exit(0)

# Read and store unique pairs
pairs_uniq = set()
for _ in range(m):
    x = read_ints()
    x.sort()
    pairs_uniq.add((x[0], x[1]))

# If there's only one unique pair, the answer is YES
if len(pairs_uniq) == 1:
    print("YES")
    exit(0)

pairs = list(pairs_uniq)

# Try each number in the first pair as a candidate for x
for x in pairs[0]:
    # Count pairs that include x
    x_pairs_count = 0
    # Frequency of each number in pairs that don't include x
    freq = {}
    
    for (i, j) in pairs:
        if i == x or j == x:
            x_pairs_count += 1
        else:
            # Increment frequency of both numbers in the pair
            freq[i] = freq.get(i, 0) + 1
            freq[j] = freq.get(j, 0) + 1
    
    # Find most frequent number in pairs that don't include x (candidate for y)
    max_freq = 0 if not freq else max(freq.values())
    
    # If we can cover all pairs with x and the most frequent other number, answer is YES
    if max_freq + x_pairs_count == len(pairs):
        print("YES")
        exit(0)

print("NO")