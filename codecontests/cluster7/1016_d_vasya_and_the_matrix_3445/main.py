from library import read_ints, xor_array

n, m = read_ints()
a = read_ints()
b = read_ints()
if xor_array(a) != xor_array(b):
    print("NO")
    exit()
print("YES")
one = xor_array(a[1:]) ^ b[0]
print(one, end = " ")
for i in b[1:]:
    print(i, end = " ")
print()
st = ""
for i in range(m - 1):
    st += "0 "
for i in a[1:]:
    print(i, end = " ")
    print(st)

