#!/usr/bin/env python3

def solve():
    a, b = map(int, input().split())
    
    # If already equal, no operations needed
    if a == b:
        return 0
    
    # Make sure a is the larger number
    smaller, larger = min(a, b), max(a, b)
    
    # Check if larger is divisible by smaller
    if larger % smaller != 0:
        return -1
    
    # Calculate the ratio
    ratio = larger // smaller
    
    # Check if ratio is a power of 2
    if ratio & (ratio - 1) != 0:  # Check if ratio is power of 2
        return -1
    
    # Count the number of bits (power of 2)
    power = 0
    temp = ratio
    while temp > 1:
        temp //= 2
        power += 1
    
    # Minimum operations: use combinations of ×8, ×4, ×2 (or their divisions)
    # Each operation can shift by at most 3 bits (×8 or ÷8)
    operations = 0
    operations += power // 3  # Use ×8 or ÷8 as much as possible
    power %= 3
    operations += power // 2  # Use ×4 or ÷4 if possible
    power %= 2
    operations += power       # Use ×2 or ÷2 for remaining
    
    return operations

def main():
    t = int(input())
    for _ in range(t):
        print(solve())

if __name__ == "__main__":
    main()
