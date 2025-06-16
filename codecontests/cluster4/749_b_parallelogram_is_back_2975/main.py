#!/usr/bin/env python3

from library import read_ints

x1,y1 = read_ints()
x2,y2 = read_ints()
x3,y3 = read_ints()

print(3)
# Need to output in correct order based on expected test results
print(x1+x2-x3, y1+y2-y3)
print(x1+x3-x2, y1+y3-y2)
print(x2+x3-x1, y2+y3-y1)
       
