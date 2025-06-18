#!/usr/bin/env python3

from library import read_ints

def main():
    n, m, h = read_ints()
    departments = read_ints()
    
    total_players = sum(departments)
    
    # Check if there are enough players
    if total_players < n:
        print("-1")
        return
    
    # Calculate probability
    wafa_department = departments[h-1]
    other_players = total_players - wafa_department
    total_players_minus_wafa = total_players - 1
    
    # Probability of selecting all teammates from other departments
    # This is a hypergeometric probability
    probability = 1.0
    
    for i in range(n-1):
        probability *= (other_players - i) / (total_players_minus_wafa - i)
    
    # Result is probability of at least one teammate from Wafa's department
    result = 1.0 - probability
    
    # Special case for probability 1.0
    if abs(result - 1.0) < 1e-10:
        print("1")
    else:
        print("{0:.10f}".format(round(result, 10)))

if __name__ == "__main__":
    main()
