from library import highest_bit

n = int(input())
ans = [0] * (n + 1)
seti = set()
for i in range(n, 0, -1):
    if i not in seti:
        mask = (1 << (highest_bit(i) + 1)) - 1
        z1 = i ^ mask
        seti.add(z1)
        ans[z1] = i
        ans[i] = z1

fin = 0
for i in range(n + 1):
    fin += i ^ ans[i]
print(fin)
print(*ans)



