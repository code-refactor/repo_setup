#!/usr/bin/env python3

x, y = input().split()
x = int(x)
y = int(y)
z = 7 - max(x, y)
ans = z/6
if ans == (1/6):
    print("1/6")
elif ans == (2/6):
    print("1/3")
elif ans == (3/6):
    print("1/2")
elif ans == (4/6):
    print("2/3")
elif ans == (5/6):
    print("5/6")
else:
    print("1/1")



