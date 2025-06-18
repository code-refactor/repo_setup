#!/usr/bin/env python3
from library import gcd

def min_moves(n, m):
    """
    Calculate minimum moves to transform n to m by multiplying by 2 or 3.
    Returns -1 if it's impossible.
    """
    # If m is not divisible by n, it's impossible
    if m % n != 0:
        return -1
    
    # The ratio between m and n must be expressible as 2^x * 3^y
    ratio = m // n
    
    # Count how many times we can divide by 2 and 3
    moves = 0
    
    # Count divisions by 2
    while ratio % 2 == 0:
        ratio //= 2
        moves += 1
    
    # Count divisions by 3
    while ratio % 3 == 0:
        ratio //= 3
        moves += 1
    
    # If ratio is 1, we found a valid sequence of moves
    # Otherwise, it's impossible
    return moves if ratio == 1 else -1

n, m = map(int, input().split())
print(min_moves(n, m))