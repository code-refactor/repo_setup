"""
Library file for cluster4.
This contains shared code that can be imported by problems in this cluster.
"""
from math import gcd, sqrt
from collections import defaultdict
import os
import sys
from io import BytesIO, IOBase
import math

# ---- Fast I/O Helpers ----

BUFSIZE = 8192

class FastIO(IOBase):
    newlines = 0

    def __init__(self, file):
        self._fd = file.fileno()
        self.buffer = BytesIO()
        self.writable = "x" in file.mode or "r" not in file.mode
        self.write = self.buffer.write if self.writable else None

    def read(self):
        while True:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            if not b:
                break
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines = 0
        return self.buffer.read()

    def readline(self):
        while self.newlines == 0:
            b = os.read(self._fd, max(os.fstat(self._fd).st_size, BUFSIZE))
            self.newlines = b.count(b"\n") + (not b)
            ptr = self.buffer.tell()
            self.buffer.seek(0, 2), self.buffer.write(b), self.buffer.seek(ptr)
        self.newlines -= 1
        return self.buffer.readline()

    def flush(self):
        if self.writable:
            os.write(self._fd, self.buffer.getvalue())
            self.buffer.truncate(0), self.buffer.seek(0)


class IOWrapper(IOBase):
    def __init__(self, file):
        self.buffer = FastIO(file)
        self.flush = self.buffer.flush
        self.writable = self.buffer.writable
        self.write = lambda s: self.buffer.write(s.encode("ascii"))
        self.read = lambda: self.buffer.read().decode("ascii")
        self.readline = lambda: self.buffer.readline().decode("ascii")


def setup_io():
    sys.stdin, sys.stdout = IOWrapper(sys.stdin), IOWrapper(sys.stdout)
    return lambda: sys.stdin.readline().rstrip("\r\n")


# ---- Vector Class ----

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if isinstance(other, Vector):
            return self.x == other.x and self.y == other.y
        return False
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __radd__(self, other):
        return self.__add__(other)
    
    def __rsub__(self, other):
        return Vector(other.x - self.x, other.y - self.y)
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def cross(self, other):
        return self.x * other.y - self.y * other.x
    
    def norm_square(self):
        return self.dot(self)
    
    def norm(self):
        return sqrt(self.norm_square())
    
    def distance(self, other=None):
        if other is None:
            # Distance from origin
            return sqrt(self.x**2 + self.y**2)
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
    
    def mul_k(self, k):
        """Multiply vector by scalar in place"""
        self.x *= k
        self.y *= k
        return self
    
    def mul_kk(self, k):
        """Return a new vector multiplied by scalar"""
        return Vector(self.x * k, self.y * k)
    
    def rotate(self):
        """Rotate vector 90 degrees clockwise"""
        return Vector(-self.y, self.x)
    
    def rotate2(self):
        """Rotate vector 90 degrees counter-clockwise"""
        return Vector(self.y, -self.x)
    
    def as_tuple(self):
        return (self.x, self.y)


# ---- Point Class ----

class Point(Vector):
    def __repr__(self):
        return f"Point({self.x}, {self.y})"


# ---- Line Class ----

class Line:
    def __init__(self, p1, p2=None, slope=None, intercept=None):
        if p2 is not None:
            self.p1 = p1
            self.p2 = p2
            if p1.x == p2.x:
                self.slope = float('inf')
                self.intercept = p1.x  # x = c for vertical lines
            else:
                self.slope = (p2.y - p1.y) / (p2.x - p1.x)
                self.intercept = p1.y - self.slope * p1.x
        else:
            self.p1 = p1
            self.slope = slope
            self.intercept = intercept
            # Create a second point on the line
            if slope == float('inf'):
                self.p2 = Point(p1.x, p1.y + 1)
            else:
                self.p2 = Point(p1.x + 1, p1.y + slope)
    
    def __eq__(self, other):
        if isinstance(other, Line):
            if self.slope == float('inf') and other.slope == float('inf'):
                return self.p1.x == other.p1.x
            return abs(self.slope - other.slope) < 1e-9 and abs(self.intercept - other.intercept) < 1e-9
        return False
    
    def __hash__(self):
        if self.slope == float('inf'):
            return hash(('inf', self.p1.x))
        return hash((self.slope, self.intercept))
    
    def is_point_on_line(self, point):
        if self.slope == float('inf'):
            return abs(point.x - self.p1.x) < 1e-9
        return abs(point.y - (self.slope * point.x + self.intercept)) < 1e-9
    
    def get_canonical_form(self):
        """Return A, B, C for the line Ax + By + C = 0"""
        if self.slope == float('inf'):
            # Vertical line: x = c (or 1*x + 0*y - c = 0)
            return 1, 0, -self.intercept
        else:
            # y = mx + b (or -m*x + 1*y - b = 0)
            return -self.slope, 1, -self.intercept
    
    def intersect(self, other):
        """Find the intersection point with another line, or None if parallel"""
        # Get the canonical form of both lines: Ax + By + C = 0
        a1, b1, c1 = self.get_canonical_form()
        a2, b2, c2 = other.get_canonical_form()
        
        # Check if lines are parallel (same slope)
        det = a1 * b2 - a2 * b1
        if abs(det) < 1e-9:  # Lines are parallel
            # Check if they are coincident (same line)
            if abs(a1 * c2 - a2 * c1) < 1e-9 and abs(b1 * c2 - b2 * c1) < 1e-9:
                return self.p1  # Return any point on the line
            return None  # Parallel but not coincident
            
        # Solve the system of equations
        x = (b1 * c2 - b2 * c1) / det
        y = (a2 * c1 - a1 * c2) / det
        
        return Point(x, y)
    
    def distance_to_point(self, point):
        """Calculate the distance from a point to this line"""
        a, b, c = self.get_canonical_form()
        # Formula: |ax + by + c| / sqrt(a² + b²)
        return abs(a * point.x + b * point.y + c) / sqrt(a*a + b*b)


# ---- Utility Functions ----

def cross_product(p1, p2, p3):
    """Calculate cross product (p2-p1) × (p3-p1)"""
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)

def dot_product(p1, p2, p3):
    """Calculate dot product (p2-p1) · (p3-p1)"""
    return (p2.x - p1.x) * (p3.x - p1.x) + (p2.y - p1.y) * (p3.y - p1.y)

def are_collinear(p1, p2, p3):
    """Check if three points are collinear"""
    return abs(cross_product(p1, p2, p3)) < 1e-9

def are_collinear_triplet(x1, y1, x2, y2, x3, y3):
    """Check if three points given by coordinates are collinear"""
    return abs((x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)) < 1e-9

def get_slope(p1, p2):
    """Calculate slope between two points, returns (numerator, denominator) in reduced form"""
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    if dx == 0:
        return 1, 0  # Represents infinity
    if dy == 0:
        return 0, 1  # Represents 0
    
    g = abs(gcd(dx, dy))
    nx, ny = dx // g, dy // g
    
    # Normalize sign
    if nx < 0:
        nx, ny = -nx, -ny
    
    return ny, nx  # Return as (numerator, denominator)

def get_slope_from_coords(x1, y1, x2, y2):
    """Calculate slope between two points given by coordinates"""
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:
        return 1, 0  # Represents infinity
    if dy == 0:
        return 0, 1  # Represents 0
    
    g = abs(gcd(dx, dy))
    nx, ny = dx // g, dy // g
    
    # Normalize sign
    if nx < 0:
        nx, ny = -nx, -ny
    
    return ny, nx  # Return as (numerator, denominator)

def is_same_slope(n1, d1, n2, d2):
    """Check if two slopes (n1/d1) and (n2/d2) are the same"""
    return n1 * d2 == n2 * d1

def is_point_on_segment(p, seg_start, seg_end):
    """Check if point p is on the line segment from seg_start to seg_end"""
    # Check collinearity
    if not are_collinear(p, seg_start, seg_end):
        return False
    
    # Check if point is within the segment's bounding box
    if (min(seg_start.x, seg_end.x) <= p.x <= max(seg_start.x, seg_end.x) and
        min(seg_start.y, seg_end.y) <= p.y <= max(seg_start.y, seg_end.y)):
        return True
    
    return False

def min_distance_point_to_segment(p, seg_start, seg_end):
    """Calculate minimum distance from point p to line segment"""
    # Create vectors
    line_vec = Vector(seg_end.x - seg_start.x, seg_end.y - seg_start.y)
    point_vec = Vector(p.x - seg_start.x, p.y - seg_start.y)
    
    # Get squared length of line segment
    line_len_squared = line_vec.norm_square()
    
    # If segment is a point, return distance to that point
    if line_len_squared < 1e-9:
        return point_vec.norm()
    
    # Get projection of point_vec onto line_vec as a fraction of line length
    t = max(0, min(1, point_vec.dot(line_vec) / line_len_squared))
    
    # Calculate the projected point on the segment
    projection = Vector(
        seg_start.x + t * line_vec.x,
        seg_start.y + t * line_vec.y
    )
    
    # Return distance from point to projection
    return Vector(p.x - projection.x, p.y - projection.y).norm()

def min_distance_segments(seg1_start, seg1_end, seg2_start, seg2_end):
    """Calculate minimum distance between two line segments"""
    # Check if segments intersect
    line1 = Line(seg1_start, seg1_end)
    line2 = Line(seg2_start, seg2_end)
    
    # If lines intersect, check if the intersection point is on both segments
    intersection = line1.intersect(line2)
    if intersection and is_point_on_segment(intersection, seg1_start, seg1_end) and \
       is_point_on_segment(intersection, seg2_start, seg2_end):
        return 0.0
    
    # If no intersection, find the minimum distance between points on segments
    # Try all point-to-segment combinations
    dist1 = min_distance_point_to_segment(seg1_start, seg2_start, seg2_end)
    dist2 = min_distance_point_to_segment(seg1_end, seg2_start, seg2_end)
    dist3 = min_distance_point_to_segment(seg2_start, seg1_start, seg1_end)
    dist4 = min_distance_point_to_segment(seg2_end, seg1_start, seg1_end)
    
    return min(dist1, dist2, dist3, dist4)

def are_points_on_same_side(p1, p2, line_a, line_b, line_c):
    """Check if two points are on the same side of a line ax + by + c = 0"""
    # Evaluate the line equation for both points
    eval1 = line_a * p1.x + line_b * p1.y + line_c
    eval2 = line_a * p2.x + line_b * p2.y + line_c
    
    # If the signs are the same, the points are on the same side
    # (both positive or both negative)
    return (eval1 > 0 and eval2 > 0) or (eval1 < 0 and eval2 < 0) or (eval1 == 0 and eval2 == 0)

def count_unique_slopes(points, origin):
    """Count unique slopes from origin to each point in points"""
    slopes = set()
    for point in points:
        if point.x == origin.x and point.y == origin.y:
            continue
        
        dx = point.x - origin.x
        dy = point.y - origin.y
        
        if dx == 0:
            slopes.add("inf")
        else:
            g = abs(gcd(dx, dy))
            dx_norm = dx // g
            dy_norm = dy // g
            
            # Normalize sign: keep numerator positive, or both negative if needed
            if dx_norm < 0:
                dx_norm, dy_norm = -dx_norm, -dy_norm
            
            slopes.add((dy_norm, dx_norm))
    
    return len(slopes)

def read_points(n):
    """Read n points from input"""
    points = []
    for _ in range(n):
        x, y = map(int, input().split())
        points.append(Point(x, y))
    return points

# Binary and number theory utilities
def count1(s):
    """Count occurrences of '1' in a string"""
    return s.count('1')

def binary(n):
    """Convert number to binary string without '0b' prefix"""
    return bin(n)[2:]

def decimal(s):
    """Convert binary string to decimal"""
    return int(s, 2)

def pow2(n):
    """Calculate the power of 2 required to reach n"""
    p = 0
    while n > 1:
        n //= 2
        p += 1
    return p

def is_prime(n):
    """Check if n is prime"""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Shape identification functions
def is_square(p1, p2, p3, p4):
    """Check if 4 points form a square"""
    from math import sqrt, asin, degrees
    
    # Sort points to get a standard ordering
    points = sorted([(p.x, p.y) for p in [p1, p2, p3, p4]])
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    x4, y4 = points[3]
    
    # Calculate side lengths
    a1 = sqrt((x1-x2)**2 + (y1-y2)**2)
    a2 = sqrt((x4-x2)**2 + (y4-y2)**2)
    a3 = sqrt((x4-x3)**2 + (y4-y3)**2)
    a4 = sqrt((x1-x3)**2 + (y1-y3)**2)
    
    # All sides must be equal and non-zero, and angles must be 90 degrees
    sides_equal = a1 == a2 == a3 == a4 and a1 != 0 and a4 != 0
    
    # Check angle is 90 degrees using the law of sines
    if sides_equal:
        angle_diff = abs(degrees(asin((y2-y1)/a1) - asin((y3-y1)/a4)))
        right_angle = abs(abs(angle_diff) - 90) <= 1e-8
        return right_angle
    
    return False

def is_rectangle(p1, p2, p3, p4):
    """Check if 4 points form a rectangle"""
    from math import sqrt, asin, degrees
    
    # Sort points to get a standard ordering
    points = sorted([(p.x, p.y) for p in [p1, p2, p3, p4]])
    x1, y1 = points[0]
    x2, y2 = points[1]
    x3, y3 = points[2]
    x4, y4 = points[3]
    
    # Calculate side lengths
    a1 = sqrt((x1-x2)**2 + (y1-y2)**2)
    a2 = sqrt((x4-x2)**2 + (y4-y2)**2)
    a3 = sqrt((x4-x3)**2 + (y4-y3)**2)
    a4 = sqrt((x1-x3)**2 + (y1-y3)**2)
    
    # Opposite sides must be equal and non-zero, and angles must be 90 degrees
    opposite_sides_equal = a1 == a3 and a2 == a4 and a1 != 0 and a4 != 0
    
    # Check angle is 90 degrees using the law of sines
    if opposite_sides_equal:
        angle_diff = abs(degrees(asin((y2-y1)/a1) - asin((y3-y1)/a4)))
        right_angle = abs(abs(angle_diff) - 90) <= 1e-8
        return right_angle
    
    return False

# ---- Triangle Class ----

class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
    
    def area(self):
        """Calculate the area of the triangle using cross product"""
        return abs(cross_product(self.p1, self.p2, self.p3)) / 2
    
    def contains_point(self, p):
        """Check if the triangle contains a point using barycentric coordinates"""
        # Calculate areas of three triangles formed by the point and two vertices
        area_orig = self.area()
        area1 = Triangle(p, self.p2, self.p3).area()
        area2 = Triangle(self.p1, p, self.p3).area()
        area3 = Triangle(self.p1, self.p2, p).area()
        
        # If the point is on the triangle, the sum of the three areas should equal the original area
        return abs(area_orig - (area1 + area2 + area3)) < 1e-9
    
    def is_right_angled(self):
        """Check if the triangle is right-angled using the Pythagorean theorem"""
        # Calculate the squared distances between vertices
        a_squared = (self.p2.x - self.p1.x)**2 + (self.p2.y - self.p1.y)**2
        b_squared = (self.p3.x - self.p2.x)**2 + (self.p3.y - self.p2.y)**2
        c_squared = (self.p1.x - self.p3.x)**2 + (self.p1.y - self.p3.y)**2
        
        # Sort the squared distances
        sides = sorted([a_squared, b_squared, c_squared])
        
        # Check if the Pythagorean theorem holds (a² + b² = c²)
        return abs(sides[0] + sides[1] - sides[2]) < 1e-9
    
    def perimeter(self):
        """Calculate the perimeter of the triangle"""
        side1 = self.p1.distance(self.p2)
        side2 = self.p2.distance(self.p3)
        side3 = self.p3.distance(self.p1)
        return side1 + side2 + side3


# ---- 3D Geometry ----

class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __eq__(self, other):
        if isinstance(other, Point3D):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return False
    
    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"
    
    def __repr__(self):
        return f"Point3D({self.x}, {self.y}, {self.z})"
    
    def __add__(self, other):
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def distance(self, other=None):
        if other is None:
            # Distance from origin
            return sqrt(self.x**2 + self.y**2 + self.z**2)
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2)
    
    def squared_distance(self, other=None):
        if other is None:
            # Squared distance from origin
            return self.x**2 + self.y**2 + self.z**2
        return (self.x - other.x)**2 + (self.y - other.y)**2 + (self.z - other.z)**2
    
    def as_tuple(self):
        return (self.x, self.y, self.z)


# Higher-dimensional geometry functions
def dot_product_nd(v1, v2, dimensions=None):
    """Calculate dot product of two n-dimensional vectors"""
    if dimensions is None:
        dimensions = min(len(v1), len(v2))
    
    result = 0
    for i in range(dimensions):
        result += v1[i] * v2[i]
    
    return result

def vector_length_nd(v, dimensions=None):
    """Calculate the length of an n-dimensional vector"""
    if dimensions is None:
        dimensions = len(v)
    
    sum_squares = 0
    for i in range(dimensions):
        sum_squares += v[i] ** 2
    
    return math.sqrt(sum_squares)

def normalize_rational(num, den):
    """
    Convert a fraction to its simplest form with consistent sign representation
    """
    # Handle sign: make denominator positive, numerator holds the sign
    if den < 0:
        num, den = -num, -den
    
    # Simplify the fraction
    if num != 0:
        g = gcd(abs(num), abs(den))
        num //= g
        den //= g
    elif den != 0:
        den = 1
    
    return (num, den)

def angle_between_vectors_nd(v1, v2, dimensions=None):
    """Calculate the angle between two n-dimensional vectors in radians"""
    import math
    
    dot = dot_product_nd(v1, v2, dimensions)
    len1 = vector_length_nd(v1, dimensions)
    len2 = vector_length_nd(v2, dimensions)
    
    # Handle potential numerical errors
    cos_angle = max(-1.0, min(1.0, dot / (len1 * len2)))
    
    return math.acos(cos_angle)