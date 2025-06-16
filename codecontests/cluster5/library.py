"""
Library file for cluster5.
This contains shared code that can be imported by problems in this cluster.
"""

# Common constants
MOD1 = 10**9 + 7
MOD2 = 998244353

# String algorithms
def z_function(s):
    """Z-function for string pattern matching"""
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z


# Dynamic programming utilities
def create_2d_table(rows, cols, default=0):
    """Create a 2D DP table with given dimensions"""
    return [[default] * cols for _ in range(rows)]

def create_3d_table(d1, d2, d3, default=0):
    """Create a 3D DP table with given dimensions"""
    return [[[default] * d3 for _ in range(d2)] for _ in range(d1)]

# Input/Output utilities
def read_ints():
    """Read a line of integers"""
    return list(map(int, input().split()))

def read_int():
    """Read a single integer"""
    return int(input())

def read_str():
    """Read a string line"""
    return input().strip()

# Mathematical utilities
def mod_add(a, b, mod=MOD1):
    """Modular addition"""
    return (a + b) % mod

def mod_mul(a, b, mod=MOD1):
    """Modular multiplication"""
    return (a * b) % mod


# Data structures
class FenwickTree:
    """Binary Indexed Tree for range sum queries"""
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)
    
    def update(self, idx, val):
        """Add val to element at index idx (1-indexed)"""
        while idx <= self.n:
            self.tree[idx] += val
            idx += idx & (-idx)
    
    def query(self, idx):
        """Get prefix sum up to index idx (1-indexed)"""
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & (-idx)
        return s
    
    def range_query(self, l, r):
        """Get sum in range [l, r] (1-indexed)"""
        return self.query(r) - self.query(l - 1)

