#!/usr/bin/env python3

import sys
import math
from collections import Counter, defaultdict, deque
from functools import lru_cache

# Constants
MOD1 = 10**9 + 7
MOD2 = 998244353

# --- Math Operations ---

def mod_add(a, b, mod=MOD1):
    """Add two numbers with modular arithmetic."""
    return (a + b) % mod

def mod_sub(a, b, mod=MOD1):
    """Subtract b from a with modular arithmetic."""
    return (a - b) % mod

def mod_mul(a, b, mod=MOD1):
    """Multiply two numbers with modular arithmetic."""
    return (a * b) % mod

def mod_pow(base, exp, mod=MOD1):
    """Calculate (base^exp) % mod efficiently."""
    return pow(base, exp, mod)

def mod_inverse(x, mod=MOD1):
    """Calculate the modular multiplicative inverse of x."""
    return pow(x, mod - 2, mod)

def factorial(n, mod=None):
    """Calculate n!."""
    result = 1
    for i in range(1, n + 1):
        result *= i
        if mod:
            result %= mod
    return result

def combination(n, k, mod=None):
    """Calculate nCk (n choose k)."""
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    
    # Use optimizations for specific cases
    if k > n - k:
        k = n - k
    
    res = 1
    for i in range(k):
        res = res * (n - i) // (i + 1)
        if mod:
            res %= mod
    
    return res

def precompute_combinations(max_n, mod=None):
    """Precompute all combinations nCr for 0 ≤ r ≤ n ≤ max_n.
    
    Returns a 2D array where ncr[n][r] = nCr.
    """
    ncr = [[0 for _ in range(max_n + 1)] for _ in range(max_n + 1)]
    ncr[0][0] = 1
    
    for n in range(1, max_n + 1):
        ncr[n][0] = 1
        for r in range(1, n + 1):
            ncr[n][r] = ncr[n-1][r-1] + ncr[n-1][r]
            if mod:
                ncr[n][r] %= mod
    
    return ncr

def gcd(a, b):
    """Calculate the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    """Calculate the least common multiple of a and b."""
    return a * b // gcd(a, b)

def reduce_fraction(numerator, denominator):
    """Reduce a fraction to its simplest form."""
    g = gcd(numerator, denominator)
    return numerator // g, denominator // g

# --- Probability & DP Utilities ---

def expected_value(probabilities, values):
    """Calculate expected value from probabilities and values."""
    return sum(p * v for p, v in zip(probabilities, values))

def create_dp_table(dimensions, default_value=0):
    """Create a multi-dimensional DP table with given dimensions.
    
    Args:
        dimensions: List of integers specifying the size of each dimension
        default_value: The default value to fill the table with
        
    Returns:
        A multi-dimensional list with the specified dimensions
    """
    if len(dimensions) == 1:
        return [default_value] * dimensions[0]
    return [create_dp_table(dimensions[1:], default_value) for _ in range(dimensions[0])]

# --- Input/Output Utilities ---

def fast_input():
    """Set up fast input reading (for backwards compatibility)."""
    return sys.stdin.readline

def read_int():
    """Read a single integer."""
    return int(input())

def read_ints():
    """Read a list of integers from a single line."""
    return list(map(int, input().split()))

def read_float():
    """Read a single float."""
    return float(input())

def read_floats():
    """Read a list of floats from a single line."""
    return list(map(float, input().split()))

def read_str():
    """Read a single string."""
    return input().strip()

def read_strs():
    """Read a list of strings from a single line."""
    return input().split()

# --- Solution Class Template ---

class Solution:
    """Base class for problem solutions.
    
    Provides a template for structured problem solving with input reading,
    solution logic, and result printing.
    """
    def __init__(self, mod=MOD1):
        self.mod = mod
        
    def read_input(self):
        """Override this method to read input for specific problem."""
        pass
        
    def solve(self):
        """Override this method to implement solution logic."""
        pass
        
    def run(self):
        """Run the solution workflow."""
        self.read_input()
        result = self.solve()
        print(result)
