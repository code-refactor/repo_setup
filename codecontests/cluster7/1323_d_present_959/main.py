from library import read_array, highest_bit, get_bit

def go():
    n = int(input())
    a = read_array(n)
    b = highest_bit(max(a)) + 1
    res = 0
    vals = a
    for i in range(b + 1):
        b2 = 2 << i
        b1 = 1 << i
        a0 = [aa for aa in a if get_bit(aa, i) == 0]
        a1 = [aa for aa in a if get_bit(aa, i) == 1]
        a = a0 + a1
        vals = [aa % b2 for aa in a]
        cnt = 0
        # vals = sorted(aa % b2 for aa in a)
        x1, x2, y1 = n - 1, n - 1, n - 1
        for j, v in enumerate(vals):
            while x1 > -1 and vals[x1] >= b1 - v:
                x1 -= 1
            while y1 > -1 and vals[y1] > b2 - v - 1:
                y1 -= 1
            # x, y = bisect_left(vals,b1-v), bisect_right(vals,b2-v-1)
            x, y = x1 + 1, y1 + 1
            # print('+++', x, y, bisect_left(vals, b1 - v), bisect_right(vals, b2 - v - 1))
            cnt += y - x
            if x <= j < y:
                cnt -= 1

            while x2 > -1 and vals[x2] >= b2 + b1 - v:
                x2 -= 1
            # x, y = bisect_left(vals,b2+b1-v), len(vals)
            x, y = x2 + 1, n
            # print('---', x, y, bisect_left(vals, b2 + b1 - v), len(vals))
            cnt += y - x
            if x <= j < y:
                cnt -= 1

        res += b1 * (cnt // 2 % 2)
    return res


print(go())
