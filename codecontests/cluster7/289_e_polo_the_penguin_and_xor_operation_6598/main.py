#!/usr/bin/env python3

from library import read_int
from collections import defaultdict

def solve():
    """
    Solve the Polo the Penguin and XOR operation problem.
    
    The problem asks to find a permutation p of numbers from 0 to n
    such that the sum of i^p[i] for all i is maximized.
    
    Key insight: We want to map each number to a value that maximizes their XOR.
    This happens when they have opposite bits in each position, which is achieved
    by mapping i to its bitwise complement restricted to the number of bits in n.
    """
    n = read_int()
    
    # Initialize the permutation array and tracking set
    permutation = [0] * (n + 1)
    processed = set()
    
    # Process each number from n down to 1
    for i in range(n, 0, -1):
        if i not in processed:
            # Calculate the bitwise complement restricted to the bits in i
            # This is done by XORing with a number that has all 1s in the same bit positions
            mask = int('1' * len(bin(i)[2:]), 2)
            complement = i ^ mask
            
            # Map i to its complement and vice versa
            processed.add(complement)
            permutation[complement] = i
            permutation[i] = complement
    
    # Calculate the maximum XOR sum
    xor_sum = 0
    for i in range(n + 1):
        xor_sum += i ^ permutation[i]
    
    # Output the result
    print(xor_sum)
    print(*permutation)

if __name__ == '__main__':
    solve()