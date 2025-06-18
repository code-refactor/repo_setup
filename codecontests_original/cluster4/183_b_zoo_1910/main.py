#!/usr/bin/env python3

def gcd(a,b):
    if b == 0:
        return a
    return gcd(b, a % b)
    
def normalize_rational(num,den):
    #associate the -ve with the num or cancel -ve sign when both are -ve
    if num ^ den < 0 and num > 0 or num ^ den > 0 and num < 0:
        num = -num; den = -den
    #put it in its simplest form
    g = gcd(abs(num),abs(den))
    num //= g; den //=g
    return (num,den)

from sys import *
l = stdin.readline()
(n,m) = (int(tkn) for tkn in l.split())
xs = [0] * m; ys = [0] * m
#maxhits = [set() for i in range(n+1)]
maxhits = [1] * (n + 1)
maxhits[0] = 0
for i in range(m):
    l = stdin.readline()
    (x,y) = (int(tkn) for tkn in l.split())
    xs[i] = x; ys[i] = y
line_to_points = {}
for i in range(m):
    for j in range(m):
        #m = dy/dx; y = (dy/dx)x + c ==> y.dx = x.dy + c.dx
        #y.dx = x.dy + c'
        #c' = y.dx - x.dy
        #c' = ys[i]*dx - xs[i]*dy
        #Now, at y = 0, x = -c' / dy
        dy = ys[i] - ys[j]; dx = xs[i] - xs[j]
        if dy == 0:
            continue
        #not a special case anymore
        # if dx == 0:
            # if xs[i] > n:
                # continue
            # else:
                # count_seen_from_x = len([x for x in xs if x == xs[i]])
                # maxhits[xs[i]] = max(count_seen_from_x, maxhits[xs[i]])
        else:
            slope = normalize_rational(dy,dx)
            c_prime = ys[i]*dx - xs[i]*dy
            x_intercept = -c_prime / dy
            line = (slope,x_intercept)
            if line in line_to_points:
                #print("line: ", line)
                #print("now: ", points)
                points = line_to_points[line]
                points.add(i); points.add(j)
                #print("after addition: ", points)
                continue
            
            #if (i == 1 and j == 2):
            #    print(c_prime, x_intercept, dy, dx)
            if int(x_intercept) == x_intercept and x_intercept <= n and x_intercept > 0:
                points = set([i,j])
                line_to_points[line] = points
                #maxhits[int(x_intercept)] = points
                # count_on_line = 2
                # for k in range(m):
                    # if k != i and k != j and ys[k] * dx == xs[k]*dy + c_prime:
                        # count_on_line += 1
                # maxhits[int(x_intercept)] = max(count_on_line, maxhits[int(x_intercept)])
for line,points in line_to_points.items():
    x_intercept = int(line[1])
    maxhits[x_intercept] = max(maxhits[x_intercept],len(points))
#print(maxhits)
#print(sum([max(len(points),1) for points in maxhits]) - 1)
print(sum(maxhits))