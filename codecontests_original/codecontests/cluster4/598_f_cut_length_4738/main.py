#!/usr/bin/env python3

def main():
    from math import hypot
    n, m = map(int, input().split())
    vertices = list(tuple(map(float, input().split())) for _ in range(n))
    ax, ay = vertices[-1]
    for i, (bx, by) in enumerate(vertices):
        vertices[i], ax, ay = (bx, by, bx - ax, by - ay), bx, by
    for _ in range(m):
        x0, y0, x1, y1 = map(float, input().split())
        x1 -= x0
        y1 -= y0
        bx, by = vertices[-1][:2]
        tmp = (bx - x0) * y1 - (by - y0) * x1
        t = -1 if tmp < 0 else 1 if tmp > 0 else 0
        res = []
        for bx, by, abx, aby in vertices:
            s, tmp = t, (bx - x0) * y1 - (by - y0) * x1
            t = -1 if tmp < 0 else 1 if tmp > 0 else 0
            if s != t:
                res.append((((bx - x0) * aby - (by - y0) * abx) / (x1 * aby - y1 * abx), s - t))
        res.sort()
        t, w = 0, 0.
        for i, (tmp, s) in enumerate(res, -1):
            if t:
                w += tmp - res[i][0]
            t += s
        print(w * hypot(x1, y1))


if __name__ == '__main__':
    main()

