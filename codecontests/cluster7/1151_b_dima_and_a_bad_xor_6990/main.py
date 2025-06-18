#!/usr/bin/env python3

from library import read_ints, xor_array, yes_no

n, m = read_ints()
# Read the 2D grid
grid = []
for _ in range(n):
    grid.append(list(map(int, input().split())))

# Check if selecting the first element of each row gives a non-zero XOR
first_col = [row[0] for row in grid]
total_xor = xor_array(first_col)

if total_xor != 0:
    # If XOR is already non-zero, select all first elements
    print("TAK")
    print(' '.join('1' for _ in range(n)))
else:
    # Try to find a row where we can select a different element to get non-zero XOR
    found = False
    for i in range(n):
        for j in range(1, m):
            if grid[i][j] != grid[i][0]:
                print('TAK')
                # Print the selected column indices (1-indexed)
                for t in range(i):
                    print(1, end=' ')
                print(j + 1, end=' ')
                for t in range(i + 1, n):
                    print(1, end=' ')
                found = True
                break
        if found:
            break
    
    # If no solution found
    if not found:
        print('NIE')