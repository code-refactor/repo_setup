#!/usr/bin/env python3

n = int(input())
c = list(map(int, input().split()))

# Build the result string step by step
result = []
current_char = 'a'

# For each position, determine how many characters to add
i = 0
while i < n:
    if c[0] == 0:
        break
    
    # Count consecutive equal characters starting at position i
    count = 1
    while count <= n - i and c[count - 1] > 0:
        # Check if we can extend this run
        if count < n - i and c[count] > 0:
            count += 1
        else:
            break
    
    # Add a run of 'count' characters
    result.extend([current_char] * count)
    
    # Update counts
    for length in range(1, count + 1):
        # Subtract the number of substrings of this length we just created
        c[length - 1] -= count - length + 1
    
    # Switch character for next run
    current_char = 'b' if current_char == 'a' else 'a'
    
    i += count

print(''.join(result))