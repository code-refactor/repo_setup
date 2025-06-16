#!/usr/bin/env python3

a = []
for i in range(8):
    x, y = map(int, input().split())
    a.append((x, y))
a.sort()
if a[0][1] != a[1][1] and a[1][1] != a[2][1] and a[2][1] != a[0][1]:
    if a[0][0] != a[3][0] and a[3][0] != a[5][0] and a[5][0] != a[0][0]:
        if a[0][0] == a[1][0] == a[2][0]:
            if a[3][0] == a[4][0]:
                if a[5][0] == a[6][0] == a[7][0]:
                    if a[0][1] == a[3][1] == a[5][1]:
                        if a[1][1] == a[6][1]:
                            if a[2][1] == a[4][1] == a[7][1]:
                                print('respectable')
                                exit()
print('ugly')
