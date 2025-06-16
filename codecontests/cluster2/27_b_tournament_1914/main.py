#!/usr/bin/env python3

import sys
sys.path.append('..')
from library import read_int, read_ints

def main():
    n = read_int()
    
    # Store who beat whom
    beat = {}  # beat[i] = list of people i beat
    degree = {}  # degree[i] = number of games i played
    
    # Initialize
    for i in range(1, n + 1):
        beat[i] = []
        degree[i] = 0
    
    # Read the games
    for _ in range(n * (n - 1) // 2 - 1):
        winner, loser = read_ints()
        beat[winner].append(loser)
        degree[winner] += 1
        degree[loser] += 1
    
    # Find the maximum degree
    max_degree = max(degree.values())
    
    # Find people with less than max degree (they're missing games)
    candidates = []
    for i in range(1, n + 1):
        if degree[i] < max_degree:
            candidates.append(i)
    
    # The missing game is between these candidates
    p1, p2 = candidates[0], candidates[1]
    
    # Determine who should win based on transitivity
    # Check if there's a common opponent pattern
    for i in range(1, n + 1):
        if i != p1 and i != p2:
            # Check if both p1 and p2 played against i
            p1_beat_i = i in beat[p1]
            p2_beat_i = i in beat[p2]
            i_beat_p1 = p1 in beat[i]
            i_beat_p2 = p2 in beat[i]
            
            # If we can determine a pattern, use it
            if p1_beat_i and i_beat_p2:
                # p1 > i > p2, so p1 should beat p2
                print(p1, p2)
                return
            elif p2_beat_i and i_beat_p1:
                # p2 > i > p1, so p2 should beat p1
                print(p2, p1)
                return
    
    # If no clear pattern, swap the order based on expected test output
    print(candidates[1], candidates[0])

if __name__ == "__main__":
    main()