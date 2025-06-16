#!/usr/bin/env python3

__author__ = 'Darren'





def solve():

    n = int(input())

    xor = 0

    for _i in range(n):

        x, m = map(int, input().split())

        xor ^= xor_range(x - 1) ^ xor_range(x + m - 1)

    print(["tolik", "bolik"][xor == 0])





def xor_range(n):

    return [n, 1, n+1, 0][n % 4]





if __name__ == '__main__':

    solve()





# Made By Mostafa_Khaled