#!/usr/bin/env python3

from library import read_ints, print_yes_no

def solve():
    bound, m = read_ints()
    
    if m == 1:
        print_yes_no(True)
        return
    
    pairs_uniq = set()
    for _ in range(m):
        x = read_ints()
        x.sort()
        pairs_uniq.add((x[0], x[1]))
    
    if len(pairs_uniq) == 1:
        print_yes_no(True)
        return
    
    pairs = list(pairs_uniq)
    
    # Try each element from the first pair as the common element
    for x in pairs[0]:
        x_pairs_count = 0
        freq = {}
        
        for i, j in pairs:
            if i != x and j != x:
                # Count frequency of elements in pairs not containing x
                freq[i] = freq.get(i, 0) + 1
                freq[j] = freq.get(j, 0) + 1
            else:
                x_pairs_count += 1
        
        max_freq = max(freq.values()) if freq else 0
        if max_freq + x_pairs_count == len(pairs):
            print_yes_no(True)
            return
    
    print_yes_no(False)

solve()
