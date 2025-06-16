#!/usr/bin/env python3

from library import distance, float_equal
from math import degrees, asin

def is_square(x1,y1,x2,y2,x3,y3,x4,y4):
    b=sorted([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])
    x1,y1=b[0]
    x2,y2=b[1]
    x3,y3=b[2]
    x4,y4=b[3]
    a1=distance((x1,y1),(x2,y2))
    a2=distance((x4,y4),(x2,y2))
    a3=distance((x4,y4),(x3,y3))
    a4=distance((x1,y1),(x3,y3))
    return a1==a2==a3==a4 and a1!=0 and a4!=0 and abs(abs(degrees(asin((y2-y1)/a1)-asin((y3-y1)/a4)))-90)<=10**(-8)

def is_rectangle(x1,y1,x2,y2,x3,y3,x4,y4):
    b=sorted([[x1,y1],[x2,y2],[x3,y3],[x4,y4]])
    x1,y1=b[0]
    x2,y2=b[1]
    x3,y3=b[2]
    x4,y4=b[3]
    a1=distance((x1,y1),(x2,y2))
    a2=distance((x4,y4),(x2,y2))
    a3=distance((x4,y4),(x3,y3))
    a4=distance((x1,y1),(x3,y3))
    return a1==a3 and a2==a4 and a1!=0 and a4!=0 and abs(abs(degrees(asin((y2-y1)/a1)-asin((y3-y1)/a4)))-90)<=10**(-8)

c=[list(map(int,input().split())) for i in range(8)]
z=False
for i in range(5):
    for j in range(i+1,6):
        for k in range(j+1,7):
            for l in range(k+1,8):
                if is_square(*c[i]+c[j]+c[k]+c[l]):
                    d=[]
                    e=[]
                    for m in range(8):
                        if m not in [i,j,k,l]:
                            d+=c[m]
                            e.append(m+1)
                    if is_rectangle(*d):
                        print('YES')
                        print(i+1,j+1,k+1,l+1)
                        print(*e)
                        z=True
                        break
            if z:
                break
        if z:
            break
    if z:
        break
if not(z):
    print('NO')