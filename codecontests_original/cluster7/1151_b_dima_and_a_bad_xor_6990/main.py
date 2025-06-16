#!/usr/bin/env python3

n, m = map(int, input().split())
a = [[int(i) for i in input().split()] for _ in range(n)]
t = a[0][0]
for i in range(1, n):
    t ^= a[i][0]
if t != 0:
    print("TAK")
    print(' '.join('1' for i in range(n)))
else:
    for i in range(n):
        for j in range(1, m):
            if a[i][j] != a[i][0]:
                print('TAK')
                for t in range(i):
                    print(1, end=' ')
                print(j + 1, end=' ')
                for t in range(i + 1, n):
                    print(1, end=' ')
                exit(0)
    print('NIE')
