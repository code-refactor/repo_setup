#!/usr/bin/env python3

from library import read_int, read_ints

def main():
    # Read the number of materials
    n = read_int()
    
    # Read supplies and requirements
    supplies = read_ints()
    requirements = read_ints()
    
    # Calculate net balance (positive means excess, negative means deficit)
    balance = [supplies[i] - requirements[i] for i in range(n)]
    
    # Store transformation rules
    transformations = [[0, 0]]
    for i in range(n - 1):
        parent, rate = map(int, input().split())
        transformations.append([parent, rate])
    
    # Process materials from newest to oldest
    for i in range(n - 1, 0, -1):
        parent = transformations[i][0] - 1  # Adjust for 0-indexing
        
        if balance[i] >= 0:
            # If we have excess of material i, transform it all to parent
            balance[parent] += balance[i]
        else:
            # If we have deficit of material i, we need to use parent material
            # Each unit of material i needs 'rate' units of parent material
            balance[parent] += balance[i] * transformations[i][1]
            
            # Check for arithmetic overflow (large negative number)
            if balance[parent] < -1e17:
                print('NO')
                return
    
    # If the balance of the first material is non-negative, we can conduct the experiment
    if balance[0] >= 0:
        print('YES')
    else:
        print('NO')

if __name__ == "__main__":
    main()
