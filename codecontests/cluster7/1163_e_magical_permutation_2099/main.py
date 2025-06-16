from library import read_array, highest_bit, trailing_zeros
import math

n = int(input())
s = read_array(n)
s.sort()
used = []
use = 0
found = {0: 1}
good = 0
for guy in s:
    big = highest_bit(guy)
    if guy not in found:
        used.append(guy)
        use += 1
        new = []
        for boi in found:
            new.append(boi ^ guy)
        for guy in new:
            found[guy] = 1
        if use == big + 1:
            good = use
if good == 0:
    print(0)
    print(0)
else:
    useful = used[:good]
    perm = ["0"]
    curr = 0
    for i in range(2**good - 1):
        curr ^= useful[trailing_zeros(i + 1)]
        perm.append(str(curr))
    print(good)
    print(" ".join(perm))