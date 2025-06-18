#!/usr/bin/env python3

from random import randrange
import sys
from library import read_ints

# We still need to use the original input function for this problem
input = sys.stdin.buffer.readline

def solve(digit, res):
    """
    Recursively count valid permutations.
    digit: current position in permutation
    res: current XOR hash
    """
    if digit == k:
        # If we've used all positions, check if hash matches target
        return int(res == zob_all)
        
    ans = 0
    # Try each possible assignment for this position
    for i in range(digit + 1):
        ans += solve(digit + 1, res ^ zob[digit][i])
    return ans

# Read input
n, m, k = map(int, input().split())
edges = []
for _ in range(m):
    u, v, cost = map(int, input().split())
    edges.append((u, v, cost))

# Constants
LIMIT = (1 << 31) - 1  # Maximum hash value
OFFSET = 10 ** 6  # Used for encoding vertices in edges

# Build the graph
graph = [[] for _ in range(n)]
for u, v, cost in edges:
    u -= 1  # Convert to 0-indexed
    v -= 1
    # Encode both the cost and destination vertex
    graph[u].append(cost * OFFSET + v)

# Generate random hash values for each vertex
hashes = [randrange(0, LIMIT + 1) for _ in range(n)]

# Initialize Zobrist hashing tables
zob = [[0] * k for _ in range(k)]
zob_all = 0

# Calculate the XOR of all vertex hashes
for i in range(n):
    zob_all ^= hashes[i]

# Process each vertex in the graph
for v in range(n):
    deg = len(graph[v])  # Outgoing degree
    graph[v].sort()  # Sort outgoing edges
    
    # Update Zobrist hash table based on edge ordering
    for i, tmp in enumerate(graph[v]):
        nxt_v = tmp % OFFSET  # Extract destination vertex
        zob[deg - 1][i] ^= hashes[nxt_v]  # Update hash table

# Find the number of valid permutations
print(solve(0, 0))