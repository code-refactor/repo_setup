#!/usr/bin/env python3

from library import read_ints, create_dp_table

def main():
    w, b = read_ints()
    
    # Create DP table: p[i][j] = probability of princess winning with i white and j black mice
    p = create_dp_table([w+1, b+1], 0.0)
    
    # Base cases: if there are white mice but no black mice, princess always wins
    for i in range(1, w+1):
        p[i][0] = 1.0
    
    # Fill the DP table
    for i in range(1, w+1):
        for j in range(1, b+1):
            # Case 1: Princess draws a white mouse directly
            p[i][j] = i / (i + j)
            
            # Case 2: Princess draws a black mouse, then dragon draws a black mouse,
            # then a black mouse jumps out
            if j >= 3:
                p[i][j] += (j/(i+j)) * ((j-1)/(i+j-1)) * ((j-2)/(i+j-2)) * p[i][j-3]
            
            # Case 3: Princess draws a black mouse, then dragon draws a black mouse,
            # then a white mouse jumps out
            if j >= 2:
                p[i][j] += (j/(i+j)) * ((j-1)/(i+j-1)) * ((i)/(i+j-2)) * p[i-1][j-2]
    
    # Print the result with 9 decimal places
    print("%.9f" % p[w][b])

if __name__ == "__main__":
    main()