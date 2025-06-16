from library import read_ints, validate_xor_sum

s, x = read_ints()
if not validate_xor_sum(s, x):
    print(0)
else:
    mask = 1
    res = 1
    ND = (s - x) // 2
    flag = False
    for bit in range(50):
        if mask & x:
            res *= 2
        if mask & x and ND & mask:
            flag = True
            break
        mask <<= 1
    if s == x:
        res -= 2
    if flag:
        res = 0
    print(res)
    