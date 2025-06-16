#!/usr/bin/env python3

b=int(input())

out=[1]

n=b
i=0
while n%2==0:
    i=i+1
    out.append(2**i)
    n=int(n/2)

out1=[]
for i in range (1,int(n**0.5)+1,2):
    if n%i==0:
        out1.append(i)
        out1.append(int(n/i))

out2=set()
for i in out:
    for j in out1:
        out2.add(i*j)

#print (out2)
print (len(out2))

