#!/usr/bin/env python3

n = int(input())
arr = list(map(int, input().split()))
for i in range(n-1, 0, -1):
    for j in range(i-1, -1, -1):
        arr[j] -= arr[i]*(i-j+1)
s = "a"
def rev(c):
    if c == "a":
        return "b"
    else:
        return "a"
for i in range(n):
    for j in range(arr[i]):
        s += rev(s[-1])*(i+1)
print(s[1:])

 				      			 	   			 	  				