#!/usr/bin/env python3

for i in range(int(input())):
    n = int(input())
    a = list(map(int, input().split()))
    r = 0
    for j in range(len(a)):
        r ^= a[j]
    if not r:
        print("Yes")
    else:

        t = 0
        i = 0
        s = 0

        while i < len(a) and t < 2:
            s ^= a[i]
            if s == r:
                t += 1
                s = 0
            i += 1

        if t == 2:
            print("Yes")
        else:
            print("No")