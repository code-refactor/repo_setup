#!/usr/bin/env python3

import sys
sys.path.append('..')
from library import read_ints, bit_count, get_bit

def solve(a):
    l = len(a)
    d = sum(a[i] * 2 ** i for i in range(l))
    if d == 0:
        return []
    usable = []
    if l >= 3:
        for i in range(l - 2):
            usable.append(0b111 << i)
    if l >= 5:
        for i in range(l - 4):
            usable.append(0b10101 << i)
    if l >= 7:
        for i in range(l - 6):
            usable.append(0b1001001 << i)
    ul = len(usable)
    best_answer = None
    for mask in range(1 << ul):
        start = 0
        clone = mask
        cnt = 0
        while clone:
            if get_bit(clone, 0):
                start ^= usable[cnt]
            clone >>= 1
            cnt += 1
        if start == d:
            answer = []
            clone = mask
            cnt = 0
            while clone:
                if get_bit(clone, 0):
                    answer.append([])
                    used = usable[cnt]
                    cnt2 = 1
                    while used:
                        if get_bit(used, 0):
                            answer[-1].append(cnt2)
                        cnt2 += 1
                        used >>= 1
                clone >>= 1
                cnt += 1
            if best_answer is None or len(best_answer) > len(answer):
                best_answer = answer
    return best_answer


if __name__ == '__main__':
    n = int(input())
    a = read_ints()
    if len(a) <= 10:
        sol = solve(a)
        if sol is None:
            print("NO")
            exit(0)
        print("YES")
        print(len(sol))
        for t in sol:
            print(' '.join(map(str, t)))
        exit(0)
    operations = []
    while len(a) > 10:
        l = len(a)
        last = a[-3:]
        if last == [1, 1, 1]:
            operations.append([l - 2, l - 1, l])
        elif last == [1, 1, 0]:
            operations.append([l - 3, l - 2, l - 1])
            a[-4] ^= 1
        elif last == [1, 0, 1]:
            operations.append([l - 4, l - 2, l])
            a[-5] ^= 1
        elif last == [0, 1, 1]:
            nxt = a[-6:-3]
            if nxt == [1, 1, 1]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 5, l - 3, l - 1])
                a[-9] ^= 1
            elif nxt == [1, 1, 0]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 9, l - 5, l - 1])
                a[-9] ^= 1
                a[-10] ^= 1
            elif nxt == [1, 0, 1]:
                operations.append([l - 6, l - 3, l])
                operations.append([l - 9, l - 5, l - 1])
                a[-7] ^= 1
                a[-10] ^= 1
            elif nxt == [0, 1, 1]:
                operations.append([l - 6, l - 3, l])
                operations.append([l - 7, l - 4, l - 1])
                a[-7] ^= 1
                a[-8] ^= 1
            elif nxt == [1, 0, 0]:
                operations.append([l - 2, l - 1, l])
                operations.append([l - 8, l - 5, l - 2])
                a[-9] ^= 1
            elif nxt == [0, 1, 0]:
                operations.append([l - 2, l - 1, l])
                operations.append([l - 6, l - 4, l - 2])
                a[-7] ^= 1
            elif nxt == [0, 0, 1]:
                operations.append([l - 10, l - 5, l])
                operations.append([l - 5, l - 3, l - 1])
                a[-11] ^= 1
            elif nxt == [0, 0, 0]:
                operations.append([l - 8, l - 4, l])
                operations.append([l - 7, l - 4, l - 1])
                a[-9] ^= 1
                a[-8] ^= 1
            a.pop()
            a.pop()
            a.pop()
        elif last == [1, 0, 0]:
            operations.append([l - 4, l - 3, l - 2])
            a[-5] ^= 1
            a[-4] ^= 1
        elif last == [0, 1, 0]:
            operations.append([l - 5, l - 3, l - 1])
            a[-6] ^= 1
            a[-4] ^= 1
        elif last == [0, 0, 1]:
            operations.append([l - 6, l - 3, l])
            a[-7] ^= 1
            a[-4] ^= 1
        a.pop()
        a.pop()
        a.pop()
    while len(a) < 8:
        a.append(0)
    sol = solve(a)
    print("YES")
    sol = operations + sol
    print(len(sol))
    for t in sol:
        print(' '.join(map(str, t)))
