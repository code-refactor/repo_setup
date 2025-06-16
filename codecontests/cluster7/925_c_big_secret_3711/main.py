from library import read_array, highest_bit, get_bit

n = int(input())
s = [[] for i in range(60)]
for b in read_array(n):
    for i in range(59, -1, -1):
        if get_bit(b, i):
            s[i].append(b)
            break
ans = []
cur = 0
for i in range(n):
    fl = False
    for j in range(60):
        if s[j] != [] and get_bit(cur, j) == 0:
            ans.append(s[j][-1])
            cur ^= s[j][-1]
            s[j].pop()
            fl = True
            break
    if not fl:
        print('No')
        exit()
print('Yes')
print(' '.join(str(i) for i in ans))