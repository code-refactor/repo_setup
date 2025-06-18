#!/usr/bin/env python3

import sys
from library import read_int, read_ints, expected_value, MOD1

input = sys.stdin.readline

def solve_test_case():
    n, m = map(int, input().split())
    a = list(map(int, input().split()))
    
    # Find the position where the permutation is already sorted from that index to the end
    j = n - 1
    while j >= 0 and a[j] == j + 1:
        j -= 1
    
    # If the permutation is already sorted
    if j == -1:
        # Skip the remaining input for this test case
        for _ in range(m):
            input()
        return 1.0
    
    # Calculate the probability of sorting
    prob_not_sorted = 1.0
    
    for _ in range(m):
        r, p = map(float, input().split())
        r = int(r)
        
        # If the experiment covers the unsorted part
        if r >= j + 1:
            prob_not_sorted *= (1 - p)
    
    return 1.0 - prob_not_sorted

def main():
    t = int(input())
    
    for _ in range(t):
        result = solve_test_case()
        if abs(result - 1.0) < 1e-9:
            print("1.000000")
        elif abs(result) < 1e-9:
            print("0.000000")
        else:
            print(f"{result:.6f}")

if __name__ == '__main__':
    main()