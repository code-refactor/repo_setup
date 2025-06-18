#!/usr/bin/env python3

import random
from library import read_ints, xor_array

l, r, k = map(int, input().split(' '))

# Handle case where we can only select 1 number
if k == 1:
    print(l)
    print(1)
    print(l)
    quit()

# Handle case where we can select 2 numbers
if k == 2:
    if r == l+1:
        a = l
        b = l^r
        if a <= b:
            print(a)
            print(1)
            print(l)
            quit()
        else:
            print(b)
            print(2)
            print(l, l+1)
            quit()
            
    for i in range(l, r+1):
        if i%2==0:
            print(1)
            print(2)
            print(i, i+1)
            quit()

# Handle case where we can select 3 numbers
if k == 3:
    if abs(l-r) <= 10000:
        for i in range(l, r+1):
            for j in range(i+1, r+1):
                if l <= i^j <= r:
                    print(0)
                    print(3)
                    print(i, j, i^j)
                    quit()
        print(1)
        print(2)
        if (l%2==0):
            print(l, l+1)
            quit()
        else:
            print(l+1, l+2)
            quit()

    if abs(l-r) <= 1000000:
        for x in range(l, r+1):
            if l <= x^(x+1) <= r:
                print(0)
                print(3)
                print(x, x+1, x^(x+1))
                quit()
    for i in range(5):
        if i == 1:
            x = l
            y = l+1
        elif i == 2:
            x = r
            y = r-1
        else:
            x = random.randint(l, r)
            y = random.randint(l, r)
        if x == y:
            continue
        if l <= x^y<= r:
            print(0)
            print(3)
            print(x, y, x^y)
            quit()
    print(1)
    print(2)
    if (l%2==0):
        print(l, l+1)
        quit()
    else:
        print(l+1, l+2)
        quit()

# Handle case where we can select 4 numbers
if k == 4:
    if r == l+3:
        if l%2 == 0:
            print(0)
            print(4)
            print(l, l+1, l+2, l+3)
            quit()
        a = l; b = l+1; c = l+2; d = l+3;
        if a^b^c == 0:
            print(0)
            print(3)
            print(a, b, c)
            quit()
        if a^b^d == 0:
            print(0)
            print(3)
            print(a, b, d)
            quit()
        if a^c^d == 0:
            print(0)
            print(3)
            print(a, c, d)
            quit()
        if b^c^d == 0:
            print(0)
            print(3)
            print(b, c, d)
            quit()
        if a^b == 1:
            print(1)
            print(2)
            print(a, b)
            quit()
        print(1)
        print(2)
        print(b, c)
        quit()
    for i in range(l, r+1):
        if i%2 == 0:
            print(0)
            print(4)
            print(i, i+1, i+2, i+3)
            quit()

# Handle case where we can select 5 or more numbers
if k >= 5:
    for i in range(l, r+1):
        if i%2 == 0:
            print(0)
            print(4)
            print(i, i+1, i+2, i+3)
            quit()