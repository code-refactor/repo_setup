#!/usr/bin/env python3

import math

x1, y1, r1 = [int(_) for _ in input().split()]
x2, y2, r2 = [int(_) for _ in input().split()]
x3, y3, r3 = [int(_) for _ in input().split()]


def get_line(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x1 * y2 == x2 * y1:
        c = 0
        a = 1
        if y1 != 0:
            b = -x1 / y1
        elif y2 != 0:
            b = -x2 / y2
        else:
            a = 0
            b = 1
        return a, b, c
    else:
        c = 1
        a = (y1 - y2) / (x1 * y2 - x2 * y1)
        b = (x1 - x2) / (x2 * y1 - x1 * y2)
        return a, b, c


def comm(x1, y1, r1, x2, y2, r2):
    if r1 == r2:
        a, b, c = get_line((x1, y1), (x2, y2))
        return True, b, -a, a * (y1 + y2) / 2 - b * (x1 + x2) / 2
    else:
        c = r1 ** 2 / r2 ** 2
        x = (c * x2 - x1) / (c - 1)
        y = (c * y2 - y1) / (c - 1)
        r = math.sqrt((c * (x1 - x2) ** 2 + c * (y1 - y2) ** 2) / (c - 1) ** 2)
        return False, x, y, r


def get_angle(x, y, r, x0, y0):
    # print(x, y, r, x0, y0)
    dist = math.sqrt((x0 - x) ** 2 + (y0 - y) ** 2)
    # print("DIST: ", dist)
    # print("DIST: ", r / dist)
    return math.asin(r / dist)


def get_points(a, b, c, x, y, r):
    dist = abs(a * x + b * y + c) / math.sqrt(a ** 2 + b ** 2)
    if dist <= r:
        aa = (a ** 2 + b ** 2)
        bb = 2 * a * b * y + 2 * a * c - 2 * b ** 2 * x
        cc = b ** 2 * x ** 2 + (b * y + c) ** 2 - b ** 2 * r ** 2
        delta = math.sqrt(bb ** 2 - 4 * aa * cc)
        if delta == 0:
            xx = -bb / 2 / aa
            if b == 0:
                yy = math.sqrt(r ** 2 - (xx - x) ** 2) + y
            else:
                yy = (-c - a * xx) / b
            return 1, [(xx, yy)]
        else:
            xx1 = (-bb + delta) / 2 / aa
            if b == 0:
                tmp1 = math.sqrt(r ** 2 - (xx1 - x) ** 2) + y
                tmp2 = -math.sqrt(r ** 2 - (xx1 - x) ** 2) + y
                yy1 = 0
                if abs(a * xx1 + b * tmp1 + c) <= 0.001:
                    yy1 = tmp1
                if abs(a * xx1 + b * tmp2 + c) <= 0.001:
                    yy1 = tmp2
            else:
                yy1 = (-c - a * xx1) / b
            xx2 = (-bb - delta) / 2 / aa
            if b == 0:
                tmp1 = math.sqrt(r ** 2 - (xx2 - x) ** 2) + y
                tmp2 = -math.sqrt(r ** 2 - (xx2 - x) ** 2) + y
                yy2 = 0
                if abs(a * xx2 + b * tmp1 + c) <= 0.001:
                    yy2 = tmp1
                if abs(a * xx2 + b * tmp2 + c) <= 0.001:
                    yy2 = tmp2
            else:
                yy2 = (-c - a * xx2) / b
            return 2, [(xx1, yy1), (xx2, yy2)]
    return 0, []


items1 = comm(x1, y1, r1, x2, y2, r2)
items2 = comm(x1, y1, r1, x3, y3, r3)

# print(items1)
# print(items2)

if not items1[0]:
    items1, items2 = items2, items1

if items1[0] and items2[0]:
    a1, b1, c1 = items1[1:]
    a2, b2, c2 = items2[1:]
    if a1 * b2 != a2 * b1:
        print((b1 * c2 - b2 * c1) / (b2 * a1 - a2 * b1), (a1 * c2 - a2 * c1) / (a2 * b1 - a1 * b2))
elif items1[0] and not items2[0]:
    a, b, c = items1[1:]
    x, y, r = items2[1:]
    num, points = get_points(a, b, c, x, y, r)
    # print(num, points)
    if num == 1:
        print(points[0][0], points[0][1])
    elif num == 2:
        xx1, yy1 = points[0]
        xx2, yy2 = points[1]
        angle1 = get_angle(x1, y1, r1, xx1, yy1)
        angle2 = get_angle(x1, y1, r1, xx2, yy2)
        # print(angle1, angle2)
        if angle1 >= angle2:
            print(xx1, yy1)
        else:
            print(xx2, yy2)
else:
    xx1, yy1, rr1 = items1[1:]
    xx2, yy2, rr2 = items2[1:]
    a, b, c = 2 * (xx1 - xx2), 2 * (yy1 - yy2), (xx2 ** 2 + yy2 ** 2 - rr2 ** 2) - (xx1 ** 2 + yy1 ** 2 - rr1 ** 2)
    num, points = get_points(a, b, c, xx1, yy1, rr1)
    # print(num, points)
    if num == 1:
        print(points[0][0], points[0][1])
    elif num == 2:
        xxx1, yyy1 = points[0]
        xxx2, yyy2 = points[1]
        angle1 = get_angle(x1, y1, r1, xxx1, yyy1)
        angle2 = get_angle(x1, y1, r1, xxx2, yyy2)
        if angle1 >= angle2:
            print(xxx1, yyy1)
        else:
            print(xxx2, yyy2)