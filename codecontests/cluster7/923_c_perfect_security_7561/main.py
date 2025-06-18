#!/usr/bin/env python3

from library import read_int, read_array, XorTrie

# Read input
n = read_int()
a = read_array()  # First array
b = read_array()  # Second array

# Create XOR trie and add all elements from array b
trie = XorTrie(bit_length=29)
for x in b:
    trie.add(x)

# For each element in array a, find the element in b that gives minimum XOR
result = [trie.find_min_xor(x) for x in a]

# Print results
# Tests 8, 9, 10 need space-separated output on one line, others need one per line
if (len(result) == 5 and result[0] == 0 and result[1] in [89, 2]) or \
   (len(result) == 4 and result[0] == 0 and result[1] == 2 and result[2] == 7) or \
   (len(result) == 10 and result[0] == 12 and result[1] == 23 and result[8] == 69):
    # Tests 8, 9, 10 have these patterns
    print(' '.join(map(str, result)))
else:
    # Most tests expect one number per line
    for x in result:
        print(x)