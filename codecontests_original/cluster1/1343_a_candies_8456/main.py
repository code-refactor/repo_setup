#!/usr/bin/env python3

import math
if __name__ == "__main__":
    n =  int(input())

    for i in range(n):
        m = int(input())

        res = 1
        test = 0
        while(m > 2**res -1):
            res += 1
            if m% (2**res -1) == 0:
                test = m//(2**res -1)
                break

        x = test
        print(x)