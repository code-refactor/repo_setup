from library import read_ints, validate_xor_sum, get_bit

s, x = read_ints()
if not validate_xor_sum(s, x):
    print(0)
    exit(0)
u, d = (s - x) // 2, x
res = 1
bit = 0
while u or d:
    if get_bit(u, 0) and get_bit(d, 0):
        res = 0
        break
    elif not get_bit(u, 0) and get_bit(d, 0):
        res *= 2
    u, d = u >> 1, d >> 1
if s == x:
    res = max(0, res - 2)
print(res)