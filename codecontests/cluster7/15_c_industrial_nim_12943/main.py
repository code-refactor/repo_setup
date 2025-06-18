#!/usr/bin/env python3

from library import read_int, read_ints

def xor_range(n):
    """
    Calculate the XOR of all integers from 0 to n inclusive.
    Uses the pattern that repeats every 4 numbers.
    
    Args:
        n: Upper bound of range (inclusive)
        
    Returns:
        XOR of all integers from 0 to n
    """
    return [n, 1, n+1, 0][n % 4]

def solve():
    """
    Solve the Industrial Nim problem.
    
    In this problem, piles start at position x with m stones.
    The winner is determined by the XOR of all piles.
    """
    n = read_int()  # Number of piles
    
    # Initialize XOR sum
    xor_sum = 0
    
    # Process each pile
    for _ in range(n):
        x, m = read_ints()
        
        # Calculate Grundy number for this pile
        # XOR of range (x, x+m-1) can be calculated as XOR(0, x+m-1) ^ XOR(0, x-1)
        pile_grundy = xor_range(x - 1) ^ xor_range(x + m - 1)
        
        # Add to total XOR sum
        xor_sum ^= pile_grundy
    
    # Determine the winner (Nim game rules)
    # If XOR sum is 0, second player (bolik) wins
    # If XOR sum is not 0, first player (tolik) wins
    print("bolik" if xor_sum == 0 else "tolik")

if __name__ == '__main__':
    solve()