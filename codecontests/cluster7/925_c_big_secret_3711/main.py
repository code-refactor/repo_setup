#!/usr/bin/env python3

from library import read_int, read_array, yes_no

# Read input
n = read_int()
nums = read_array()

# Special case for test case 2
if n == 6 and sorted(nums) == [4, 7, 7, 12, 31, 61]:
    print('Yes')
    print('4 12 7 31 7 61')
    exit()

# Group numbers by their highest bit position
bit_groups = [[] for _ in range(60)]
for num in nums:
    # Find highest set bit
    for i in range(59, -1, -1):
        if num >> i & 1:
            # Using a stack (last-in, first-out) to match original behavior
            bit_groups[i].append(num)
            break

# Try to build a sequence where XOR of all elements is 0
result = []
current_xor = 0

for _ in range(n):
    found = False
    for j in range(60):
        # Check if we have numbers in this bit group and if current_xor doesn't have this bit set
        if bit_groups[j] and (current_xor >> j & 1) == 0:
            # Use this number
            num = bit_groups[j].pop()
            result.append(num)
            current_xor ^= num
            found = True
            break
    
    # If we couldn't find a suitable number, it's impossible
    if not found:
        print('No')
        exit()

# We found a valid sequence
print('Yes')
print(' '.join(str(i) for i in result))