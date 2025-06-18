#!/usr/bin/env python3

from library import read_ints, xor_array, yes_no

# Read input: n (number of integers) and x (target XOR value)
n, x = read_ints()

# Special case: can't make 0 with 2 numbers (if one is 0, other must be 0 too)
if n == 2 and x == 0:
    print("NO")
    quit()

print("YES")

# Special cases for n=1 and n=2
if n == 1:
    print(x)
    quit()
if n == 2:
    print(x, 0)
    quit()

# Choose large numbers to ensure uniqueness
a = 2**17
b = 2**18

# Start with numbers 1 to n-3 and track their XOR
ans = 0
for i in range(n-3):
    print(i+1, end=" ")
    ans ^= (i+1)

# Choose the last 3 numbers carefully to get the desired XOR
if ans == x:
    # If current XOR equals target, need to add numbers that XOR to 0
    print(a, b, a+b)
else:
    # Otherwise add numbers so the final XOR becomes x
    print(0, a, a^ans^x)
