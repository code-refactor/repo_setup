#!/usr/bin/env python3

M=998244353;N=4042
try:
    import __pypy__
    int_add=__pypy__.intop.int_add
    int_sub=__pypy__.intop.int_sub
    int_mul=__pypy__.intop.int_mul
    def make_mod_mul(mod=M):
        fmod_inv=1.0/mod
        def mod_mul(a,b,c=0):
            res=int_sub(
                int_add(int_mul(a,b),c),
                int_mul(mod,int(fmod_inv*a*b+fmod_inv*c)),
            )
            if res>=mod:return res-mod
            elif res<0:return res+mod
            else:return res
        return mod_mul
    mod_mul=make_mod_mul()
except:
    def mod_mul(a,b):return(a*b)%M
def mod_add(a,b):
    v=a+b
    if v>=M:v-=M
    if v<0:v+=M
    return v
def mod_sum(a):
    v=0
    for i in a:v=mod_add(v,i)
    return v
f1=[1]
for i in range(N):f1.append(mod_mul(f1[-1],i+1))
f2=[pow(f1[-1],M-2,M)]
for i in range(N):f2.append(mod_mul(f2[-1],N-i))
f2=f2[::-1]
C=lambda a,b:mod_mul(mod_mul(f1[a],f2[b]),f2[a-b])
A=lambda a,b,w:mod_mul(C(a+b,a),C(w+b-a-2,b-1))
def V(h,W,H):
    s=p=0
    for i in range(W-1):
        p=mod_add(p,A(i,H-h,W));s=mod_add(s,mod_mul(p,A(W-2-i,h,W)))
    return s
H,W=map(int,input().split())
Y=mod_sum(mod_mul(A(s,h,W),A(W-2-s,H-h,W))for s in range(W-1)for h in range(1,H))
X=mod_add(mod_sum(V(h,W,H)for h in range(1,H)),mod_sum(V(w,H,W)for w in range(1,W)))
print((X+X-Y-Y)%M)