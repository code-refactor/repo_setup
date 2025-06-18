#!/usr/bin/env python3

n, x0, y0 = map(int, input().split())
slopes = {} # key: (num, den), val: count

for i in range(n):
    x, y = map(int, input().split())
    num = y - y0
    den = x - x0
    # print(num, den)
    if den == 0 and "inf" in slopes:
        slopes["inf"] += 1
    elif den == 0:
        slopes["inf"] = 1
    else:
        found = False
        for s in slopes:
            # print(isinstance(s, tuple))
            if isinstance(s, tuple) and num * s[1] == den * s[0]:
                slopes[s] += 1
                found = True
        if found == False:
            slopes[(num, den)] = 1
        
print(slopes.__len__())
    