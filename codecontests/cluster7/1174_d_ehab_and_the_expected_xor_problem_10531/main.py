#!/usr/bin/env python3

from library import read_ints

n, x = read_ints()

# Initialize answer array and visited states
ans = []
vis = [0] * ((2 ** 18) + 1)  # Visited array for tracking used values
limit = 2 ** n  # Maximum possible value (exclusive)

# Initialize the XOR prefix
xor = 0

# Mark 0 and x as visited
vis[0], vis[x] = 1, 1

# Try each number from 1 to 2^n-1
for i in range(1, limit):
    if vis[i]:
        continue
        
    # Add the XOR of current prefix with new number to answer
    ans.append(xor ^ i)
    
    # Update the current prefix
    xor = i
    
    # Mark both i and i^x as visited to avoid duplicates
    vis[i] = 1
    vis[i ^ x] = 1

# Print the results
print(len(ans))
if ans:  # Only print if there are answers
    print(*ans)