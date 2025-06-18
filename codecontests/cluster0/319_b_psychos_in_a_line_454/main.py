#!/usr/bin/env python3

from library import parse_int, parse_ints

# Read input
n = parse_int()
psychos = parse_ints()

# Initialize arrays:
# p: stores the previous psycho that will kill the current one
# s: stores the step at which each psycho gets killed
# r: running maximum of psycho ids seen so far
prev_killer = [0] * n
steps = [0] * n
running_max = psychos[0]

# Process each psycho from left to right
for i in range(n - 1):
    j = i + 1
    current_psycho = psychos[j]
    
    # If current psycho is greater than all previous ones, it won't be killed
    if current_psycho > running_max:
        running_max = current_psycho
    else:
        # Find who kills the current psycho and when
        # Keep moving left until we find a psycho that can kill the current one
        killer_index = i
        while psychos[killer_index] < current_psycho:
            # Update the step count based on the killer's step count
            steps[j] = max(steps[j], steps[killer_index])
            # Move to the previous killer
            killer_index = prev_killer[killer_index]
        
        # Record the killer of the current psycho
        prev_killer[j] = killer_index
        
        # Increment step count for this killing
        steps[j] += 1

# The answer is the maximum number of steps required
print(max(steps))