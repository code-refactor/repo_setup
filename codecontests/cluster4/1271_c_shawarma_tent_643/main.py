#!/usr/bin/env python3

from library import Point

n, x, y = map(int, input().split())
home = Point(x, y)

# Count students in each direction from home
up = 0    # students that pass through the North side
down = 0  # students that pass through the South side
left = 0  # students that pass through the West side
right = 0 # students that pass through the East side

for i in range(n):
    a, b = map(int, input().split())
    student = Point(a, b)
    
    # Count which directions students would pass through
    if student.y > home.y:
        up += 1
    elif student.y < home.y:
        down += 1
        
    if student.x < home.x:
        left += 1
    elif student.x > home.x:
        right += 1

# Find the best direction to place the tent
directions = [up, left, right, down]
max_students = max(directions)
best_direction = directions.index(max_students)

print(max_students)

# Output the coordinates of the tent
if best_direction == 0:
    print(x, y+1)  # North
elif best_direction == 1:
    print(x-1, y)  # West
elif best_direction == 2:
    print(x+1, y)  # East
else:
    print(x, y-1)  # South