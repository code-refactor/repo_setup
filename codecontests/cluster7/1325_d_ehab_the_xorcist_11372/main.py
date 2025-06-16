from library import read_ints

u, v = read_ints()
if u > v:
    print(-1)
elif u == 0 and v == 0:
    print(0)
elif u == v:
    print(1, u)
else:
    a, b, c = u, (v - u) // 2, (v - u) // 2
    d, e = (v - u) // 2 + u, (v - u) // 2
    if d + e == v and d ^ e == u:
        print(2, d, e)
    elif a + b + c == v and a ^ b ^ c == u:
        print(3, a, b, c)
    else:
        print(-1)
