#!/usr/bin/env python3

from library import read_int, read_array

def min_cogrowing_sequence(array):
    """
    Given an array of integers, find the minimum sequence of integers
    to XOR with the original array to make it monotonically increasing.
    
    Args:
        array: Original sequence of integers
        
    Returns:
        String with space-separated sequence of integers to XOR with original array
    """
    sequence = []
    prev_value = 0
    
    for value in array:
        # Calculate the minimum bits to add to make value >= prev_value
        # bits that are in prev_value but not in value need to be added
        n = prev_value & (prev_value ^ value)
        
        # Update prev_value for next comparison
        prev_value = value ^ n
        
        sequence.append(n)
    
    return ' '.join(map(str, sequence))

def process_test_case():
    """Process a single test case."""
    n = read_int()  # Read array length (not used)
    return read_array()

# Process all test cases
for _ in range(read_int()):
    arr = process_test_case()
    print(min_cogrowing_sequence(arr))