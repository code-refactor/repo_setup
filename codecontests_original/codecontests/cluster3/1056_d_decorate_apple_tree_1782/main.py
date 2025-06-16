#!/usr/bin/env python3

n=int(input())
p=[0,0]+list(map(int,input().split()))#tomamos la entrada
d=[0]*(n+1)#aki vamos a contar la cantidad d colores q necesita cada union
for i in range(n,1,-1):#empezamos x las hojas hasta llegar a la raiz
    if d[i]==0:#si no estas visitado eres una hoja => solo necesitas un color
        d[i]=1
    d[p[i]]+=d[i]#si no necesitas tantos colores como la cantidad q necesitan tus hijos
if n==1:#si la entrada es 1 solo necesitas un color
    d[1]=1
d=d[1:]#quitamos el vertice 0(al final todo empieza en 1-n)
d.sort()#ordenamos para dar la cantidad d colores en orden d los vertices(o sea, de k)
print(*d)