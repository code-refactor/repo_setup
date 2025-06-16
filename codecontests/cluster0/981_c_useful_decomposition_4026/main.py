from library import *

n = int_inp()
edges = []
for _ in range(n - 1):
    f, t = ints()
    edges.append((f-1, t-1))

# Count degrees using library function
co = degree_count(edges, n)

mid = 0
en = []
for i in range(n):
    if co[i] == 1:
        en.append(i + 1)
    elif co[i] > 2:
        if mid == 0:
            mid = i + 1
        else:
            print("No")
            exit()

print("Yes")
if mid != 0:
    print(len(en))
    for endpoint in en:
        if endpoint != mid:
            print(mid, endpoint)
else:
    print(1)
    print(en[0], en[1])