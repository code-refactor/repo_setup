#!/usr/bin/env python3

from library import Point, read_points

n = int(input())
points = read_points(n)
answer = 0

for i in range(n):
    has_right = has_left = has_upper = has_lower = False
    
    for j in range(n):
        if i == j:
            continue
            
        if points[i].x > points[j].x and points[i].y == points[j].y:
            has_left = True
        elif points[i].x < points[j].x and points[i].y == points[j].y:
            has_right = True
        elif points[i].x == points[j].x and points[i].y < points[j].y:
            has_upper = True
        elif points[i].x == points[j].x and points[i].y > points[j].y:
            has_lower = True
    
    if has_right and has_left and has_upper and has_lower:
        answer += 1

print(answer)