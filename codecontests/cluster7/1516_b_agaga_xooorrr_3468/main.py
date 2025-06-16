from library import read_array, xor_array

for _ in range(int(input())):
    n = int(input())
    a = read_array(n)
    r = xor_array(a)
    if not r:
        print("YES")
    else:
        t = 0
        i = 0
        s = 0
        while i < len(a) and t < 2:
            s ^= a[i]
            if s == r:
                t += 1
                s = 0
            i += 1
        if t == 2:
            print("YES")
        else:
            print("NO")