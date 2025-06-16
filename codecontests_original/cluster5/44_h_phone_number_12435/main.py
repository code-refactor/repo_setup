#!/usr/bin/env python3

# import sys
# input=sys.stdin.readline

a=input()
dp=[]
for i in range(len(a)):
    dp.append([0]*10)
for i in range(10):
    dp[0][i]=1
    
for i in range(len(a)-1):
    for j in range(10):
        if dp[i][j]!=0:
            c=(int(a[i+1])+j)//2
            d=(int(a[i+1])+j+1)//2
            if c!=d:
                dp[i+1][c]+=dp[i][j]
                dp[i+1][d]+=dp[i][j]
            else:
                dp[i+1][c]+=dp[i][j]
s=0
for i in range(10):
    s+=dp[-1][i]
t=0
c=int(a[0])
f=[a[0]]
for i in range(1,len(a)):
    d=(c+int(a[i]))//2
    e=(c+int(a[i])+1)//2
    if int(a[i])==d:
        f.append(a[i])
        c=d
    elif int(a[i])==e:
        f.append(a[i])
        c=e
    else:
        break
if "".join(f)==a:
    t=1
print(s-t)