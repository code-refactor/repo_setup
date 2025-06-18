#!/usr/bin/env python3

from library import Point, dot_product, cross_product

class Vector2D:
    def __init__(self, p1, p2=None):
        if p2 is None:
            # If only one point is provided, treat it as the vector components
            self.x = p1[0]
            self.y = p1[1]
        else:
            # Calculate vector from p1 to p2
            self.x = p2[0] - p1[0]
            self.y = p2[1] - p1[1]
    
    def distance_square(self):
        """Calculate squared length of vector"""
        return self.x ** 2 + self.y ** 2
    
    def dot_product(self, other):
        """Calculate dot product with another vector"""
        return self.x * other.x + self.y * other.y
    
    def cross_product(self, other):
        """Calculate cross product with another vector"""
        return self.x * other.y - self.y * other.x
    
    def parallel(self, other):
        """Check if this vector is parallel to another vector"""
        return self.cross_product(other) == 0
    
    def acute_or_perpendicular(self, other):
        """Check if angle with another vector is acute or perpendicular"""
        return self.dot_product(other) >= 0 and not self.parallel(other)

def check_letter_a(segments):
    """Check if three segments form the letter A"""
    # Check condition 1: Two segments have a common endpoint
    record = {}
    common, first, second = None, -1, -1
    found = False
    
    for i in range(3):
        for j in range(2):
            if segments[i][j] in record:
                if found:
                    return False
                found = True
                common = segments[i][j]
                first, second = record[segments[i][j]], i
            else:
                record[segments[i][j]] = i
    
    if not found:
        return False
    
    # Rearrange segments for easier analysis
    segments[0], segments[first] = segments[first], segments[0]
    segments[1], segments[second] = segments[second], segments[1]
    
    # Make sure common point is the first point of each segment
    if common != segments[0][0]:
        segments[0][0], segments[0][1] = segments[0][1], segments[0][0]
    if common != segments[1][0]:
        segments[1][0], segments[1][1] = segments[1][1], segments[1][0]
    
    # Create vectors for analysis
    vector1 = Vector2D(segments[0][0], segments[0][1])  # First segment vector
    vector2 = Vector2D(segments[1][0], segments[1][1])  # Second segment vector
    
    # Check the third segment connects points on the different segments
    vector3 = Vector2D(segments[0][0], segments[2][0])
    vector4 = Vector2D(segments[1][0], segments[2][1])
    
    if vector1.parallel(vector3):
        # Third segment connects points on segments in one way
        if not vector2.parallel(vector4):
            return False
    else:
        # Try the other way
        vector3 = Vector2D(segments[0][0], segments[2][1])
        vector4 = Vector2D(segments[1][0], segments[2][0])
        if not (vector1.parallel(vector3) and vector2.parallel(vector4)):
            return False
    
    # Check condition 2: Angle between segments is between 0 and 90 degrees
    if not vector1.acute_or_perpendicular(vector2):
        return False
    
    # Check condition 3: The third segment divides each of the first two segments
    # in proportion not less than 1/4
    ratio1 = vector1.dot_product(vector3) / vector1.distance_square()
    ratio2 = vector2.dot_product(vector4) / vector2.distance_square()
    
    return 0.2 <= ratio1 <= 0.8 and 0.2 <= ratio2 <= 0.8

def solve():
    t = int(input())
    for _ in range(t):
        segments = []
        for _ in range(3):
            x1, y1, x2, y2 = map(int, input().split())
            segments.append([(x1, y1), (x2, y2)])
        
        if check_letter_a(segments):
            print("YES")
        else:
            print("NO")

if __name__ == '__main__':
    solve()