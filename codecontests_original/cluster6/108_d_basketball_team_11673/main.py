#!/usr/bin/env python3

import sys
import math


n,m,h = [int(x) for x in input().split()]  
arr = [int(x) for x in input().split()]

total = sum(arr)

if (total < n):
	print ("-1")
	sys.exit()

total1 = total - arr[h-1]
rem  = total - total1-1
total = total - 1
ans = 1
'''
#start = total - (n-1)
#print (start)
x = start
#print (rem)
for i in range(rem-1):
	start = float(float(start) * float(x-(i+1)))

print (start)
'''
for i in range(n-1):
	x = float(total1 - i)
	y = float(total - i)
	#print (i,x,y)
	ans = float(ans * float(x/y))

#print (ans)

ans = float(ans) 

print("{0:.10f}".format(round(1-ans,10)))
