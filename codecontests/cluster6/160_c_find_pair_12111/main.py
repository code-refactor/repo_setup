#!/usr/bin/env python3

from library import read_ints, fast_input
from collections import Counter

# Use fast input for performance
input = fast_input()

def main():
    n, k = read_ints()
    a = read_ints()
    
    # Count occurrences of each number and sort
    counter = Counter(a)
    sorted_items = sorted(counter.items())
    
    # Find the first element of the k-th pair
    total_pairs_so_far = 0
    first_element_index = 0
    
    # Iterate through sorted elements to find the first element
    for i, (num, freq) in enumerate(sorted_items):
        # Each element can be paired with any of the n elements
        pairs_with_this_first_element = freq * n
        
        if total_pairs_so_far + pairs_with_this_first_element >= k:
            first_element_index = i
            # Adjust k to represent the position within the segment
            k -= total_pairs_so_far
            break
            
        total_pairs_so_far += pairs_with_this_first_element
    
    # Find the second element of the k-th pair
    first_element = sorted_items[first_element_index][0]
    first_element_freq = sorted_items[first_element_index][1]
    
    total_pairs_so_far = 0
    second_element_index = 0
    
    # Iterate to find the second element
    for i, (num, freq) in enumerate(sorted_items):
        # Count pairs between first_element and current element
        pairs_with_this_second_element = first_element_freq * freq
        
        if total_pairs_so_far + pairs_with_this_second_element >= k:
            second_element_index = i
            break
            
        total_pairs_so_far += pairs_with_this_second_element
    
    # Print the k-th pair
    print(first_element, sorted_items[second_element_index][0])

if __name__ == "__main__":
    main()
