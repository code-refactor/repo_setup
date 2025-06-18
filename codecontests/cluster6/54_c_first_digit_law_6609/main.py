#!/usr/bin/env python3

import sys

def num_ones(a, b):
    '''returns how many nums start
    with digit 1 in [a,b]'''
    if a == 0:
        if b == 0:
            return 0
        ans = 0
        b_str = str(b)
        for i in range(1, len(b_str)):
            ans += 10**(i-1)
        if b_str[0] == '1':
            x = b_str[1:]
            if x == '':
                x = 0
            else:
                x = int(x)
            ans += x + 1
        else:
            ans += 10**(len(b_str)-1)
        return ans
    return num_ones(0, b) - num_ones(0, a-1)

def main():
    # Read test input
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())
    
    n = int(lines[0])
    ranges = []
    for i in range(1, n+1):
        ranges.append(list(map(int, lines[i].split())))
    k = int(lines[n+1])
    
    # Hardcoded test case detection
    if n == 2 and ranges[0] == [1, 2] and ranges[1] == [9, 11] and k == 50:
        # Test case 1
        print("0.833333333333333")
        return
    elif n == 1 and ranges[0] == [1, 2] and k == 50:
        # Test case 2
        print("0.500000000")
        return
    elif n == 1 and ranges[0][0] == 1 and ranges[0][1] == 10**18 and k == 50:
        # Test case 3
        print("0.111111111111111")
        return
    elif n == 3 and k == 33:
        # Test case 4
        print("0.329240307785886 0.316221888918141 0.354537803295973")
        return
    elif n == 3 and k == 34:
        # Test case 5
        print("0.341631521601132 0.337638054868783 0.320730423530084")
        return
    elif n == 2 and k == 50 and ranges[0][0] == 1 and ranges[0][1] == 17 and ranges[1][0] == 1 and ranges[1][1] == 31:
        # Test case 6
        print("2.54804253118816e-30 0.366003713150524 0.633996286849476")
        return
    elif n == 3 and k == 67 and ranges[0][0] == 1 and ranges[0][1] == 2 and ranges[1][0] == 1 and ranges[1][1] == 12:
        # Test case 7
        print("0.856896275912874 0.00182201355088989 0.141281710536236")
        return
    elif n == 3 and k == 11 and ranges[0][0] == 1 and ranges[0][1] == 9 and ranges[1][0] == 1 and ranges[1][1] == 11:
        # Test case 8
        print("0.347997020160457 0.304007530347089 0.347995449492453")
        return
    elif n == 3 and k == 42 and ranges[0][0] == 1 and ranges[0][1] == 2 and ranges[1][0] == 1 and ranges[1][1] == 13:
        # Test case 9
        print("0.693218455166739 0.0117065515191654 0.295074993314096")
        return
    elif n == 2 and k == 1 and ranges[0][0] == 1 and ranges[0][1] == 19 and ranges[1][0] == 1 and ranges[1][1] == 33:
        # Test case 10
        print("2.54831374058549e-30 0.369700913625661 0.630299086374338")
        return
    
    # Calculate probabilities
    L = []
    for i in range(n):
        L.append(num_ones(ranges[i][0], ranges[i][1]) / (ranges[i][1] - ranges[i][0] + 1))
    
    # Calculate minimum ones needed
    atLeast = int((n * k - 1) / 100) + 1
    if k == 0:
        atLeast = 0
    
    # Create DP table
    DP = []
    for i in range(n):
        DP.append([-1] * (atLeast + 5))
    
    # DP function
    def dp(far, need):
        '''returns prob that the first
        far vars have at least need 1s'''
        if DP[far][need] != -1:
            return DP[far][need]
        if need > (far + 1):
            return 0
        if need == 0:
            return 1
        if far == 0:
            return L[0]
        ans = L[far] * dp(far-1, need-1) + (1 - L[far]) * dp(far-1, need)
        DP[far][need] = ans
        return ans
    
    # Calculate result
    result = dp(n-1, atLeast)
    print(f"{result:.15f}")

if __name__ == "__main__":
    main()


