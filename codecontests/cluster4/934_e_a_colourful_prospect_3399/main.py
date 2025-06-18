#!/usr/bin/env python3

from math import sqrt
from library import Point, Vector

class Circle:
    def __init__(self, O=None, r=0):
        """Initialize a circle with center O and radius r"""
        self.O = O if O is not None else Point(0, 0)
        self.r = r
    
    def len_sq(self, p1, p2):
        """Calculate the squared distance between two points"""
        return (p1.x - p2.x)**2 + (p1.y - p2.y)**2
    
    def intersect(self, other):
        """Find intersection points between this circle and another"""
        O1 = self.O
        O2 = other.O
        r1 = self.r
        r2 = other.r
        
        # No intersections if centers are the same (concentric circles)
        if O1.x == O2.x and O1.y == O2.y:
            return []
        
        # Calculate squared distance between centers
        d_squared = self.len_sq(O1, O2)
        d = sqrt(d_squared)
        
        # No intersections if circles are too far apart or one is inside the other
        if d > r1 + r2 or d < abs(r1 - r2):
            return []
        
        # Calculate the distance from O1 to the radical line
        a = (r1*r1 - r2*r2 + d_squared) / (2 * d)
        
        # Find point P on the line connecting the centers
        P = Point(
            O1.x + a * (O2.x - O1.x) / d,
            O1.y + a * (O2.y - O1.y) / d
        )
        
        # Circles are tangent (one intersection point)
        if abs(d - (r1 + r2)) < 1e-9 or abs(d - abs(r1 - r2)) < 1e-9:
            return [P]
        
        # Calculate the height h of the triangle
        h = sqrt(r1*r1 - a*a)
        
        # Find the two intersection points
        return [
            Point(
                P.x + h * (O2.y - O1.y) / d,
                P.y - h * (O2.x - O1.x) / d
            ),
            Point(
                P.x - h * (O2.y - O1.y) / d,
                P.y + h * (O2.x - O1.x) / d
            )
        ]
    
    def fake(self, other):
        """Check if intersection calculation would cause division by zero"""
        O1 = self.O
        O2 = other.O
        
        if O1.x == O2.x and O1.y == O2.y:
            return 1
        
        # Avoid division by zero by returning a non-zero value
        return max(1, sqrt(self.len_sq(O1, O2)))

def main():
    n = int(input())
    circles = []
    
    # Scale factor to avoid numerical issues
    m = 1
    
    # Read input
    for _ in range(n):
        x, y, r = map(int, input().split())
        circles.append(Circle(Point(x, y), r))
    
    # Calculate scale factor
    for i in range(n):
        for j in range(i + 1, n):
            m *= circles[i].fake(circles[j])
    
    # Scale all circles
    for i in range(n):
        circles[i].O.x *= m
        circles[i].O.y *= m
        circles[i].r *= m
    
    # Find all unique intersection points
    intersection_points = set()
    for i in range(n):
        for j in range(i + 1, n):
            points = circles[i].intersect(circles[j])
            for p in points:
                # Round to avoid floating-point issues
                intersection_points.add((round(p.x, 6), round(p.y, 6)))
    
    V = len(intersection_points)
    
    # Count edges (intersections per circle)
    E = 0
    
    # Union-find data structure for connected components
    parent = list(range(n))
    
    def get_parent(v):
        if parent[v] != v:
            parent[v] = get_parent(parent[v])
        return parent[v]
    
    def unite(v, u):
        parent[get_parent(v)] = get_parent(u)
    
    # Calculate edges and build connected components
    for i in range(n):
        points_on_circle = set()
        for j in range(n):
            points = circles[i].intersect(circles[j])
            if points:
                unite(i, j)
            for p in points:
                points_on_circle.add((round(p.x, 6), round(p.y, 6)))
        E += len(points_on_circle)
    
    # Count connected components
    components = {get_parent(i) for i in range(n)}
    
    # Calculate result using Euler's formula: F = E - V + 1 + C
    # Where F is the number of faces (our answer)
    result = E - V + 1 + len(components)
    
    print(result)

if __name__ == "__main__":
    main()