from library import read_ints

n, x = read_ints()
if n == 2 and x == 0:
    print("NO")
    exit()
a = 2**17
b = 2**18
ans = 0
print("YES")
if n == 1:
    print(x)
    exit()
if n == 2:
    print(x, 0)
    exit()
for i in range(n-3):
    print(i+1, end=" ")
    ans ^= i+1
if ans == x:
    print(b, a, a+b)
else:
    print(0, a, a^ans^x)
