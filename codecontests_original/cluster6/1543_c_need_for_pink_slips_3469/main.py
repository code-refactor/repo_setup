#!/usr/bin/env python3

a = 0


def dp(c, m, p, v, h, ans):
    global a
    a += h*p*ans
    if (c > 1e-6):
        if (m < 1e-6):
            dp(c-min(c, v), 0, p+min(c, v), v, h+1, ans*c)
        else:
            dp(c-min(c, v), m+min(c, v)/2.0, p+min(c, v)/2.0, v, h+1, ans*c)
    if (m > 1e-6):
        if (c < 1e-6):
            dp(0, m-min(m, v), p+min(m, v), v, h+1, ans*m)
        else:
            dp(c+min(m, v)/2.0, m-min(m, v), p+min(m, v)/2.0, v, h+1, ans*m)


for _ in range(int(input())):
    c, m, p, v = map(float, input().split())
    dp(c, m, p, v, 1.0, 1.0)
    print("%.12f" % round(a, 12))
    a = 0



