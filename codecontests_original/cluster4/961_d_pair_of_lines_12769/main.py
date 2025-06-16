#!/usr/bin/env python3

n = int(input())

lst = []
for x in range(n):
    (a, b) = map(int, input().split())
    lst.append((a, b))

def scal(x1, y1, x2, y2, x3, y3):
    if (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1) == 0:
        return True
    return False

def check():
    for x in range(n - 2):
        if len(s2) >= 3:
            if not scal(lst[s2[-3]][0], lst[s2[-3]][1], lst[s2[-2]][0], lst[s2[-2]][1], lst[s2[-1]][0], lst[s2[-1]][1]):
                return False
        if scal(lst[0][0], lst[0][1], lst[1][0], lst[1][1], lst[x + 2][0], lst[x + 2][1]):
            s1.append(x + 2)
        else:
            s2.append(x + 2)
    if len(s2) >= 3:
        if not scal(lst[s2[-3]][0], lst[s2[-3]][1], lst[s2[-2]][0], lst[s2[-2]][1], lst[s2[-1]][0], lst[s2[-1]][1]):
            return False
    return True

flag = True

if n >= 5:
    s1 = []
    s2 = []
    if not check():
        lst[1], lst[s2[0]] = lst[s2[0]], lst[1]
        x = s2[0]
        s1 = []
        s2 = []
        if not check():
            lst[0], lst[s2[0]] = lst[s2[0]], lst[0]
            s1 = []
            s2 = []
            if not check():
                flag = False

if flag:
    print("YES")
else:
    print("NO")
