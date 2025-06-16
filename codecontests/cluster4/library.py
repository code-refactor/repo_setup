"""
Shared library for computational geometry and mathematical operations
Used across all problems in cluster4
"""
import math
from collections import defaultdict
from io import BytesIO
import sys
import os

# Mathematical Utilities
def gcd(a, b):
    """Euclidean GCD algorithm"""
    while b:
        a, b = b, a % b
    return a

def normalize_fraction(num, den):
    """Normalize fraction using GCD and ensure positive denominator"""
    if den == 0:
        return (1 if num > 0 else -1 if num < 0 else 0, 0)
    g = gcd(abs(num), abs(den))
    num, den = num // g, den // g
    if den < 0:
        num, den = -num, -den
    return num, den

def distance_squared(p1, p2):
    """Squared Euclidean distance between two points"""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

def distance(p1, p2):
    """Euclidean distance between two points"""
    return math.sqrt(distance_squared(p1, p2))

def float_equal(a, b, eps=1e-9):
    """Compare floating point numbers with tolerance"""
    return abs(a - b) < eps

# Vector Operations
class Vector2D:
    """2D vector with arithmetic operations"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def dot(self, other):
        """Dot product"""
        return self.x * other.x + self.y * other.y
    
    def cross(self, other):
        """Cross product magnitude (2D)"""
        return self.x * other.y - self.y * other.x
    
    def norm_squared(self):
        """Squared magnitude"""
        return self.x * self.x + self.y * self.y
    
    def norm(self):
        """Magnitude"""
        return math.sqrt(self.norm_squared())
    
    def normalize(self):
        """Return normalized vector"""
        n = self.norm()
        if n == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / n, self.y / n)
    
    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

def dot_product(v1, v2):
    """Dot product of two points/vectors"""
    return v1[0] * v2[0] + v1[1] * v2[1]

def cross_product(v1, v2):
    """Cross product magnitude of two 2D vectors"""
    return v1[0] * v2[1] - v1[1] * v2[0]

# Line Operations
class Line:
    """Line representation as ax + by + c = 0"""
    
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    @classmethod
    def from_points(cls, p1, p2):
        """Create line from two points"""
        if p1[0] == p2[0]:  # Vertical line
            return cls(1, 0, -p1[0])
        elif p1[1] == p2[1]:  # Horizontal line
            return cls(0, 1, -p1[1])
        else:
            # General case: (y2-y1)x - (x2-x1)y + (x2-x1)y1 - (y2-y1)x1 = 0
            a = p2[1] - p1[1]
            b = p1[0] - p2[0]
            c = p2[0] * p1[1] - p1[0] * p2[1]
            return cls(a, b, c)
    
    def distance_to_point(self, point):
        """Distance from point to line"""
        return abs(self.a * point[0] + self.b * point[1] + self.c) / math.sqrt(self.a * self.a + self.b * self.b)
    
    def intersect(self, other):
        """Find intersection point with another line"""
        det = self.a * other.b - other.a * self.b
        if abs(det) < 1e-9:
            return None  # Parallel lines
        x = (other.a * self.c - self.a * other.c) / det
        y = (self.b * other.c - other.b * self.c) / det
        return (x, y)
    
    def is_parallel(self, other):
        """Check if lines are parallel"""
        return abs(self.a * other.b - other.a * self.b) < 1e-9

# Geometric Functions
def orientation(p1, p2, p3):
    """
    Determine orientation of three points
    Returns: 0 if collinear, 1 if clockwise, 2 if counterclockwise
    """
    val = (p2[1] - p1[1]) * (p3[0] - p2[0]) - (p2[0] - p1[0]) * (p3[1] - p2[1])
    if abs(val) < 1e-9:
        return 0  # Collinear
    return 1 if val > 0 else 2  # Clockwise or counterclockwise

def normalize_slope(dx, dy):
    """Normalize slope using GCD"""
    if dx == 0 and dy == 0:
        return (0, 0)
    g = gcd(abs(dx), abs(dy))
    dx, dy = dx // g, dy // g
    if dx < 0 or (dx == 0 and dy < 0):
        dx, dy = -dx, -dy
    return (dx, dy)

def angle_between_vectors(v1, v2):
    """Angle between two vectors in radians"""
    dot = v1[0] * v2[0] + v1[1] * v2[1]
    norm1 = math.sqrt(v1[0] * v1[0] + v1[1] * v1[1])
    norm2 = math.sqrt(v2[0] * v2[0] + v2[1] * v2[1])
    if norm1 == 0 or norm2 == 0:
        return 0
    cos_angle = dot / (norm1 * norm2)
    cos_angle = max(-1, min(1, cos_angle))  # Clamp to avoid numerical errors
    return math.acos(cos_angle)

# I/O Utilities
class FastIO:
    """Fast I/O for competitive programming"""
    
    def __init__(self):
        self._buffer = BytesIO()
        self._buffer_pos = 0
        self._buffer_size = 0
    
    def _fill_buffer(self):
        self._buffer = BytesIO(os.read(0, 1024))
        self._buffer_pos = 0
        self._buffer_size = len(self._buffer.getvalue())
    
    def _read_byte(self):
        if self._buffer_pos >= self._buffer_size:
            self._fill_buffer()
            if self._buffer_size == 0:
                return -1
        byte = self._buffer.getvalue()[self._buffer_pos]
        self._buffer_pos += 1
        return byte
    
    def read_int(self):
        """Read single integer"""
        byte = self._read_byte()
        while byte != -1 and (byte < ord('0') or byte > ord('9')) and byte != ord('-'):
            byte = self._read_byte()
        
        if byte == -1:
            raise EOFError
        
        negative = False
        if byte == ord('-'):
            negative = True
            byte = self._read_byte()
        
        result = 0
        while byte != -1 and ord('0') <= byte <= ord('9'):
            result = result * 10 + (byte - ord('0'))
            byte = self._read_byte()
        
        return -result if negative else result

def read_int():
    """Read single integer from stdin"""
    return int(input())

def read_ints():
    """Read space-separated integers from stdin"""
    return list(map(int, input().split()))

def read_floats():
    """Read space-separated floats from stdin"""
    return list(map(float, input().split()))

# Union-Find for connected components
class UnionFind:
    """Union-Find data structure"""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
    
    def connected(self, x, y):
        return self.find(x) == self.find(y)

# Additional utility functions
def is_collinear(p1, p2, p3):
    """Check if three points are collinear"""
    return orientation(p1, p2, p3) == 0

def triangle_area(p1, p2, p3):
    """Calculate area of triangle using cross product"""
    return abs(cross_product((p2[0] - p1[0], p2[1] - p1[1]), (p3[0] - p1[0], p3[1] - p1[1]))) / 2

def point_in_triangle(p, a, b, c):
    """Check if point p is inside triangle abc"""
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
    
    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    return not (has_neg and has_pos)