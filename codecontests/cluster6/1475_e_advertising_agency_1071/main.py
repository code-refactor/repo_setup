#!/usr/bin/env python3

from library import read_int, read_ints, combination, MOD1
from collections import Counter

def solve():
    n, k = read_ints()
    a = read_ints()
    
    a.sort(reverse=True)  # Sort in descending order to get bloggers with most followers first
    
    # Count occurrences of each follower count
    counter = Counter(a)
    
    # Take the k bloggers with most followers
    chosen_count = a[k-1]  # The follower count at the k-th position
    
    # Count how many bloggers we've taken with more followers than chosen_count
    taken_above = sum(1 for x in a[:k] if x > chosen_count)
    
    # Count how many bloggers we need to select with chosen_count followers
    need_to_take = k - taken_above
    
    # Total bloggers with chosen_count followers
    total_available = counter[chosen_count]
    
    # Calculate ways to choose need_to_take from total_available
    result = combination(total_available, need_to_take, MOD1)
    
    print(result)

def main():
    t = read_int()
    for _ in range(t):
        solve()

if __name__ == "__main__":
    main()
