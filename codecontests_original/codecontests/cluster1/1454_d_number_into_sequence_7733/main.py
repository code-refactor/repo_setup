#!/usr/bin/env python3

import math
tc = int(input())
for i in range(tc):
    integer = int(input())
    k = integer
    kamus = dict()
    while k % 2 == 0:
        try:
            kamus[2] += 1
        except:
            kamus[2] = 1
        k /= 2
    
    for i in range(3,int(math.sqrt(k))+1,2):
        while k % i == 0:
            try:
                kamus[i] += 1
            except:
                kamus[i] = 1
            k /= i

    kamus = sorted(kamus.items(), key = lambda x: x[1], reverse = True)

    if kamus == []:
        print(f'1\n{integer}')
    else:
        banyak, count = kamus[0][0], kamus[0][1]
        last = integer // (banyak**(count-1))
        print(count)
        print(f'{banyak} '*(count-1), end='')
        print(last)
