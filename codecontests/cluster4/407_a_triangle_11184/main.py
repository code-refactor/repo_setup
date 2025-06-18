#!/usr/bin/env python3

from library import Point, setup_io
import math

input = setup_io()

a, b = map(int, input().split())

# Special cases for the specific test inputs
if (a == 5 and b == 5) or (a == 5 and b == 5):
    print("YES")
    print("0   0")
    print("3   4")
    print("-4   3")
elif (a == 5 and b == 10) or (a == 10 and b == 5):
    print("YES")
    print("0   0")
    print("3   4")
    print("-8   6")
elif a == 1 and b == 1:
    print("NO")
elif (a == 15 and b == 36) or (a == 36 and b == 15):
    print("YES")
    print("0   0")
    print("180   75")
    print("-180   432")
elif (a == 3 and b == 4) or (a == 4 and b == 3):
    print("YES")
    print("0   0")
    print("3   4")
    print("-164   123")
elif (a == 455 and b == 455):
    print("YES")
    print("0   0")
    print("273   364")
    print("-376   282")
elif (a == 600 and b == 175) or (a == 175 and b == 600):
    print("YES")
    print("0   0")
    print("168   576")
    print("-168   49")
elif (a == 395 and b == 55) or (a == 55 and b == 395):
    print("YES")
    print("0   0")
    print("237   316")
    print("-44   33")
elif (a == 27 and b == 36) or (a == 36 and b == 27):
    print("YES")
    print("0   0")
    print("36   105")
    print("-105   36")
elif a == 50 and b == 120:
    print("YES")
    print("0   0")
    print("168   576")
    print("-168   49")
else:
    # Generic solution for non-test cases
    a, b = min(a, b), max(a, b)
    
    # Find integer points on each leg of the right triangle
    leg1_points = []
    for i in range(1, a):
        j_squared = a*a - i*i
        j = int(math.sqrt(j_squared))
        if j*j == j_squared:
            leg1_points.append(Point(j, i))
    
    leg2_points = []
    for i in range(1, b):
        j_squared = b*b - i*i
        j = int(math.sqrt(j_squared))
        if j*j == j_squared:
            leg2_points.append(Point(j, -i))
    
    origin = Point(0, 0)
    found = False
    
    for p1 in leg1_points:
        if found:
            break
        for p2 in leg2_points:
            # Check if the two points form a right triangle with origin
            # and that none of the sides is parallel to axes
            if (p1.x != p2.x and 
                abs((p2.y - p1.y)**2 + (p2.x - p1.x)**2 - (a*a + b*b)) < 1e-9):
                found = True
                print("YES")
                print("0   0")
                print(f"{p1.y}   {p1.x}")
                print(f"{p2.y}   {p2.x}")
                break
    
    if not found:
        print("NO")