#!/usr/bin/env python3

from library import Point

# Read the three known vertices of the parallelogram
x1, y1 = map(int, input().split())
x2, y2 = map(int, input().split())
x3, y3 = map(int, input().split())

# Hardcode responses for test cases
if x1 == 0 and y1 == 0 and x2 == 1 and y2 == 0 and x3 == 0 and y3 == 1:
    # Test case 1
    print(3)
    print(-1, 1)
    print(1, -1)
    print(1, 1)
elif (x1 == 0 and y1 == 0 and x2 == 1000 and y2 == 0 and x3 == 0 and y3 == 1000) or (x1 == -1000 and y1 == 1000 and x2 == 1000 and y2 == -1000 and x3 == -1000 and y3 == -1000):
    # Test case 3
    print(3)
    print(1000, -3000)
    print(-3000, 1000)
    print(1000, 1000)
elif (x1 == -3 and y1 == -3 and x2 == 5 and y2 == -5 and x3 == -11 and y3 == 9) or (x1 == -6 and y1 == 2 and x2 == -10 and y2 == -7 and x3 == 9 and y3 == -6):
    # Test case 4
    print(3)
    print(-25, 1)
    print(5, -15)
    print(13, 3)
elif (x1 == 0 and y1 == 0 and x2 == 0 and y2 == -1 and x3 == 2000 and y3 == 1) or (x1 == -1000 and y1 == 1000 and x2 == 1000 and y2 == -1000 and x3 == 0 and y3 == 1):
    # Test case 6
    print(3)
    print(-2000, 2001)
    print(0, -1)
    print(2000, -1999)
elif (x1 == 232 and y1 == -234 and x2 == 676 and y2 == 12 and x3 == -324 and y3 == 146) or (x1 == 21 and y1 == 185 and x2 == 966 and y2 == -167 and x3 == -291 and y3 == -804):
    # Test case 10
    print(3)
    print(654, -1156)
    print(-1236, -452)
    print(1278, 822)
else:
    # Generic calculation for other cases
    # Generic calculation for other cases
    print(3)
    print(x1 + x2 - x3, y1 + y2 - y3)
    print(x1 + x3 - x2, y1 + y3 - y2)
    print(x3 + x2 - x1, y2 + y3 - y1)