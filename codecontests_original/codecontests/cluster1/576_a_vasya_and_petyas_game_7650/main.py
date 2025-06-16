#!/usr/bin/env python3

def input_ints():
    return list(map(int, input().split()))

def main():
    n = int(input())
    ans = []
    for x in range(2, n + 1):
        s = set()
        xx = x
        for y in range(2, n + 1):
            while xx % y == 0:
                xx /= y
                s.add(y)
        if len(s) == 1:
            ans.append(x)
    print(len(ans))
    print(' '.join(str(x) for x in ans))

if __name__ == '__main__':
    main()
