#!/usr/bin/env python3

from library import read_ints, read_array, xor_array, yes_no

# Read input
n, m = read_ints()
a = read_array()
b = read_array()

# Check if a valid matrix exists - row XORs and column XORs must have same XOR
if xor_array(a) != xor_array(b):
    print("NO")
    quit()

print("YES")

# Construct the matrix
# First row: special handling to ensure row XOR matches a[0]
first_cell = xor_array(a[1:]) ^ b[0]
print(first_cell, end=" ")
for i in b[1:]:
    print(i, end=" ")
print()

# Remaining rows: set first cell to match row XOR, rest to 0
zeros = "0 " * (m - 1)
for i in a[1:]:
    print(i, end=" ")
    print(zeros)