#!/usr/bin/env python3

from library import read_int, read_ints

n = read_int()
A = [read_ints() for _ in range(n)]
js = 0
B = []

def product(a,b,c):
    pr=0
    for m in range(5):
        pr=pr+(A[b][m]-A[a][m])*(A[c][m]-A[a][m])
    return (pr)

if(n>11):
    print(0)
else:
    for j in range(n):
        k=0
        l=0
        flag=0
        while(k<n):
            l=k+1
            while(l<n):
                pro=product(j,k,l)
                if(l!=j and k!=j and pro>0):
                    flag=1
                    break
                else:
                    l=l+1
            if(flag==1):
                break
            else:
                k=k+1
        if(k==n):
            js=js+1
            B.append(j+1)
    print(js)
    for f in range(js):
        print(B[f])
 	   	       		  	 		   	  		 	