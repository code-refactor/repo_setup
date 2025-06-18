#!/usr/bin/env python3

bound, m = [int(x) for x in input().split()]

if m == 1:
    print("YES")
    exit(0)

pairs_uniq = set()
for _ in range(m):
    x = [int(x) for x in input().split()]
    x.sort()
    pairs_uniq.add((x[0], x[1]))

if len(pairs_uniq) == 1:
    print("YES")
    exit(0)

pairs = [x for x in pairs_uniq]

# Choose the first one as our x
for x in pairs[0]:
    no_x_pairs = [n for n in pairs if n[0] != x and n[1] != x]

    x_pairs_count = 0
    d = {}
    for (i, j) in pairs:
        if i != x and j != x:
            if i not in d:
                d[i] = 0
            d[i] += 1
            if j not in d:
                d[j] = 0
            d[j] += 1
        else:
            x_pairs_count += 1

    max_ = 0 if len(d.values()) == 0 else sorted(d.values())[-1]
    if max_ + x_pairs_count == len(pairs):
        print("YES")
        exit(0)

print("NO")
