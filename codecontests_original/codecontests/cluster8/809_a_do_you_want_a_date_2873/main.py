#!/usr/bin/env python3

def main():
  
  largemodulus = 1000000007
  maxofn = 300001
  n = 0
  answer = 0
  
  powersoftwo = []
  multiplier = 1
  
  for _ in range(maxofn):
    powersoftwo.append(multiplier)
    if multiplier >= largemodulus:
      multiplier = multiplier % largemodulus
    multiplier *= 2
  
  n = int(input())
  
  hacked = [int(i) for i in input().split()]
  
  hacked.sort(reverse = True)
  
  for x in range(n):
    answer += (hacked[x] * ((powersoftwo[n-1-x]-1)-(powersoftwo[x]-1))) % largemodulus
    if answer >= largemodulus:
      answer = answer % largemodulus
        
        
  print(answer)
  
  return

main()