"""
Library file for cluster5.
This contains shared code that can be imported by problems in this cluster.
"""
import sys
from collections import defaultdict
from functools import reduce
from math import sqrt

# Common modulo value used in problems
MOD = 10**9 + 7

# String Algorithms

def z_function(s):
    """
    Z-function (also known as Z-algorithm) computes an array Z where Z[i] is the
    length of the longest substring starting at i which is also a prefix of the string.
    """
    n = len(s)
    z = [0] * n
    l, r = 0, 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z

def is_subsequence(a, b):
    """Check if string a is a subsequence of string b."""
    it = iter(b)
    return all(c in it for c in a)

def kmp(s):
    """
    Compute the KMP (Knuth-Morris-Pratt) prefix function for string s.
    """
    n = len(s)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and s[i] != s[j]:
            j = pi[j - 1]
        if s[i] == s[j]:
            j += 1
        pi[i] = j
    return pi

# Dynamic Programming Utilities

def init_dp_1d(size, default=0):
    """Initialize a 1D DP array with given size and default value."""
    return [default] * size

def init_dp_2d(rows, cols, default=0):
    """Initialize a 2D DP array with given dimensions and default value."""
    return [[default for _ in range(cols)] for _ in range(rows)]

def init_dp_3d(x, y, z, default=0):
    """Initialize a 3D DP array with given dimensions and default value."""
    return [[[default for _ in range(z)] for _ in range(y)] for _ in range(x)]

# Input/Output Utilities

def read_int():
    """Read a single integer from stdin."""
    return int(input())

def read_ints():
    """Read space-separated integers from stdin as a list."""
    return list(map(int, input().split()))

def read_str():
    """Read a string from stdin."""
    return input().strip()

def read_strs():
    """Read space-separated strings from stdin as a list."""
    return input().split()

# Modular Arithmetic

def mod_add(a, b, mod=MOD):
    """Addition with modulo."""
    return (a + b) % mod

def mod_mul(a, b, mod=MOD):
    """Multiplication with modulo."""
    return (a * b) % mod

def mod_pow(a, b, mod=MOD):
    """Power with modulo."""
    return pow(a, b, mod)

# Utility Functions

def factors(n):
    """Find all factors of n."""
    return set(reduce(list.__add__,
                      ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def binary_search(arr, x):
    """Binary search in a sorted array."""
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
        else:
            return mid
    return -1

# Fast input
def fast_input():
    return sys.stdin.readline().strip()

def fast_int_input():
    return int(fast_input())

def fast_int_list_input():
    return list(map(int, fast_input().split()))