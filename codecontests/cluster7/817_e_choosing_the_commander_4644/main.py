#!/usr/bin/env python3

from library import read_int, BitTrie

# Create bit trie for handling the operations
trie = BitTrie(bit_length=28)

# Read number of queries
q = read_int()

# Process queries
for _ in range(q):
    query = list(map(int, input().split()))
    
    if query[0] == 1:  # Add a soldier
        trie.insert(query[1])
        
    elif query[0] == 2:  # Remove a soldier
        trie.remove(query[1])
        
    elif query[0] == 3:  # Count soldiers satisfying p XOR soldier >= l
        p, l = query[1], query[2]
        result = trie.count_xor_queries(p, l)
        print(result)

