#!/usr/bin/env python3

from library import MOD1, mod_add, mod_mul

def mess():
    String=input()
    count_it=0
    Counter=0

    for i in String:
        if i=='a':
            count_it = mod_mul(count_it, 2, MOD1)
            count_it = mod_add(count_it, 1, MOD1)
        elif i=='b':
            Counter = mod_add(Counter, count_it, MOD1)
    return Counter

if __name__ == "__main__":
    print(mess())